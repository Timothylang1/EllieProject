from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from math import sin, atan, log2, exp, log, pi
import tkinter

import urllib.request

from io import BytesIO
from PIL import Image

from time import sleep

def setUpDriver():
    """Sets up chromedriver that will manage all of the mapping with google. You can use the driver multiple times for different maps
    but once done, you have to call driver.quit() to close the application."""
    s=Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])     # Gets rid of google's automated software button
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver


def map(addresses, filePathWay, driver):
    """Gets a pdf map given a list of address with city
    addresses: list of addresses
    filePathWay: the pathway for the file to be saved into
    fillInColor: what color it will create the icon or fill in the buildings"""
    # ------------------------------------- CHANGE SO THAT IT DOESN'T CRASH IF NO ADDRESS IS GIVEN
    addressCoor = getCoordinates(addresses) # Gets dictionary of address (key) to coor [x, y] STORED IN A DICTIONARY

    if len(addressCoor) == 0: # If it couldn't find any addresses or no addresses were given, stops the rest of the program
        return

    # Finds the minX, maxX, minY, maxY for plotting on the map so that the map scales enough to fit all the addresses in the list
    # Initial values are all set on the first entry in the map
    minX, maxX, minY, maxY = getMinMax(addressCoor)

    # Gets the computer width and height for comparisons
    computerWidth, computerHeight = getWidthHeight()

    # Gets the required width of the map to fit all of the coordinates on it in pixels (relative to the 2048 x 2042 google map)
    # The computer width and computer height are only for scaling the y coordinate to x
    requiredWidth = getRequiredPixelWidthOfMap(minX, maxX, minY, maxY, computerWidth, computerHeight)
    
    # Gets scale of map using the requiredWidth relative to the 2048 pixel map and this computer's pixel width
    z = calculateZ(computerWidth, requiredWidth)

    # When it zooms in too much, it can't accurately plot the data. The map also become useless if zoomed in to far.
    # At z = 19, buildings start to be labeled, so the fill in method doesn't work properly, so the maximum zoom allowed is 18
    if z >= 19:
        z = 18

    # Gets center lat and long of pixels
    centerLat, centerLong = getCenterLatLong(minX, maxX, minY, maxY)

    # Gets pdf ImageGrab of map centered around lat and long scaled in by z
    png = getMap(centerLat, centerLong, z, driver)
    pixelMap = png.load()

    # Calculates the width of the image on the 2048 x 2042 scale. Because z can only be an integer, I rounded down the calculated answer so that it zoomms out a bit more than it needs to
    actualWidth = calculatePixelWidth(computerWidth, z)

    # Other nessecary data for plotting on pdf
    centerX = (maxX + minX) / 2
    centerY = (maxY + minY) / 2
    width = png.width
    height = png.height

    # Calculate offset (what x value becomes x = 0 on the png, what y value becomes y = 0 on the png)
    offsetX = centerX - actualWidth / 2
    offsetY = centerY - ((actualWidth * height) / width) / 2 # Find out the actual height by multiplying the width with the ratio between width and height of the image

    # Calculate scale factor between google's map size pixel and pdf size pixel
    ratio = width / actualWidth

    # Fill in color for icons, chose by the little firefly
    fillInColor = (197, 121, 224, 255)

    # Modifies map by adding in icons at locations on the png
    # Calculating the location
    for address in addressCoor:
        x = addressCoor[address][0]
        y = addressCoor[address][1]
        pixelX = round((x - offsetX) * ratio)
        pixelY = round((y - offsetY) * ratio)
        if z >= 17: # When z is greater than or equal to 17, we can start to see buildings, so it's safe to use the fillin
            # If drawing the box would be bigger (i.e. change more pixels), then we draw the box instead (16 x 16)
            if fillIn(pixelX, pixelY, pixelMap, width, height, fillInColor) < 256: # If something stopped fillIn (like name covering up building, or the building is too small), just revert back to the box shape
                drawSquare(pixelX, pixelY, pixelMap, width, height, fillInColor)
        else: # In every other case, we just put a 5x5 pixel box of this color where the place is
            drawSquare(pixelX, pixelY, pixelMap, width, height, fillInColor)

    # Save modified png image to new filePathWay
    png.save(filePathWay)


def drawSquare(centerX, centerY, png, width, height, endColor):
    """Modifies the pixels in png to a black 5x5 pixel box centered around centerX, centerY. Width and height variables are the width
    and height of the png"""
    # Ensure that we're not going out of bounds. If we are, shift the starting center of the x and y so that's it within the image
    centerX = max(centerX, 8) # Left bound
    centerX = min(centerX, width - 8) # Right bound
    centerY = max(centerY, 8) # Upper bound
    centerY = min(centerY, height - 8) # Lower bound
    for i in range(-8, 8):
        for j in range(-8, 8):
            png[centerX + i, centerY + j] = endColor


def fillIn(centerX, centerY, png, width, height, endColor):
    """Uses a recursive method, changes the surrounding area to the same color as long the building is all the same color. Returns how many 
    pixels it filled in that color"""
    coorlist = [(centerX, centerY)]
    startingColor = png[centerX, centerY]
    if startingColor == endColor: # If the starting color equals the end color, then the box for the nextdoor icon overflowed onto this building, so we just create another box at this place
        coorlist = []
    png[centerX, centerY] = endColor
    totalPixelsChanged = 1
    while len(coorlist) != 0:
        (x, y) = coorlist.pop(0)
        if x + 1 < width:
            if png[x + 1, y] == startingColor:
                png[x + 1, y] = endColor
                coorlist.append((x + 1, y))
                totalPixelsChanged += 1
        if x - 1 >= 0:
            if png[x - 1, y] == startingColor:
                png[x - 1, y] = endColor
                coorlist.append((x - 1, y))
                totalPixelsChanged += 1
        if y + 1 < height:
            if png[x, y + 1] == startingColor:
                png[x, y + 1] = endColor
                coorlist.append((x, y + 1))
                totalPixelsChanged += 1
        if y - 1 >= 0:
            if png[x, y - 1] == startingColor:
                png[x, y - 1] = endColor
                coorlist.append((x, y - 1))
                totalPixelsChanged += 1
    return totalPixelsChanged

    
def calculatePixelWidth(pixelWidthOfComputer, z):
    """Given the z and pixelWidth of computer, calculates how many pixels wide the image is on a 2048 x 2042 scale (Google Map scale)"""
    return ((float) (pixelWidthOfComputer)) / (2**(z - 3))
    

def calculateZ(pixelWidthOfComputer, pixelWidthRequired):
    """Given the required pixelwidth (i.e. the maximum distance between the two farthest coordinates) and the computers
    starting pixelWidth,  calculate how much google maps has to zoom in to get as close to that pixel width as possible.
    Rounds z down since as z gets bigger, we zoom in more, so rather zoom out a bit more than zoom in. Also ensures that z
    is an int since google maps can only become an int"""
    if (pixelWidthRequired == 0): # If there is no pixelWidthRequired, that means that there is only one item in the list, so we zoom in to default google maps zoom
        return 17
    return (int) (log2(pixelWidthOfComputer/pixelWidthRequired) + 3)


def getMinMax(addressCoor):
    """Returns list in this order: minX, maxX, minY, maxY given the dictionary of addresses and their cartesian coordinates."""
    # Initial values are all set on the first entry in the map
    [x, y] = list(addressCoor.items())[0][1]
    minX = x
    maxX = x
    minY = y
    maxY = y
    for address in addressCoor:
        x = addressCoor[address][0]
        y = addressCoor[address][1]
        minX = min(minX, x)
        maxX = max(maxX, x)
        minY = min(minY, y)
        maxY = max(maxY, y)

    return minX, maxX, minY, maxY


def getRequiredPixelWidthOfMap(minX, maxX, minY, maxY, computerWidth, computerHeight):
    """Given the min/max of the x and y as well as the comptuer dimensions, calculate what the pixel width of the map needs to be to include
    all coordinates relative to the 2048 x 2042 google map. It translates the pixelWidth in the y direciton to the x direction before comparing to the x coordinates"""
    return max(maxX - minX, (maxY - minY) * computerWidth / computerHeight)


def getCoordinates(addresses):
    """Gets all of the (x, y) given a list of addresses. Also contains a list of addresses that didn't have coordinates"""
    removedAddress = [] # List of all the addresses that we couldn't locate
    addressCoor = {} # Dictionary containing address -> [lat, long]

    for address in addresses:
        address = address.replace(" ", "+") + "/"
        try:
            web = urllib.request.urlopen("https://www.google.com/maps/search/" + address)
            data = str(web.read())

            initialCoor = data.find("center=") + 7
            middlePlace = data.find("%2C", initialCoor)
            endPlace = data.find("&amp", middlePlace)

            lat = float(data[initialCoor : middlePlace])
            long = float(data[middlePlace + 3 : endPlace])

            addressCoor[address] = convertGeoToPixel(lat, long, 2048, 2048 - 6.708898963677029, -180, 180, -85) # Top y coordinate came from determining what height it needs to be for lat +85 to be at y = 0
            print(address + " found and calculated")
        except:
            print(address + " not found")
            removedAddress.append(address) # Couldn't find address if there were no floating point numbers (that would be where the error occurs)
    return addressCoor


def getCenterLatLong(pixelminX, pixelmaxX, pixelminY, pixelmaxY):
    """Returns the center lat, long coordinates"""
    return convertPixelToGeo((pixelmaxX + pixelminX) / 2, (pixelmaxY + pixelminY) / 2, 2048, 2048 - 6.708898963677029, -180, 180, -85)


def convertGeoToPixel(latitude, longitude,
                  mapWidth, # in pixels
                  mapHeight, # in pixels
                  mapLngLeft, # in degrees. the longitude of the left side of the map (i.e. the longitude of whatever is depicted on the left-most part of the map image)
                  mapLngRight, # in degrees. the longitude of the right side of the map
                  mapLatBottom): # in degrees.  the latitude of the bottom of the map

    mapLatBottomRad = mapLatBottom * pi / 180
    latitudeRad = latitude * pi / 180
    mapLngDelta = (mapLngRight - mapLngLeft)

    worldMapWidth = ((mapWidth / mapLngDelta) * 360) / (2 * pi)
    mapOffsetY = (worldMapWidth / 2 * log((1 + sin(mapLatBottomRad)) / (1 - sin(mapLatBottomRad))))

    x = (longitude - mapLngLeft) * (mapWidth / mapLngDelta)
    y = mapHeight - ((worldMapWidth / 2 * log((1 + sin(latitudeRad)) / (1 - sin(latitudeRad)))) - mapOffsetY)

    return [x, y]

def convertPixelToGeo(x, y, mapWidth, mapHeight, mapLngLeft, mapLngRight, mapLatBottom):
    mapLatBottomRad = mapLatBottom * pi / 180
    mapLngDelta = (mapLngRight - mapLngLeft)
    worldMapRadius = mapWidth / mapLngDelta * 360/(2 * pi);    
    mapOffsetY = (worldMapRadius / 2 * log( (1 + sin(mapLatBottomRad) ) / (1 - sin(mapLatBottomRad))))
    equatorY = mapHeight + mapOffsetY 
    a = (equatorY-y)/worldMapRadius

    lat = 180/pi * (2 * atan(exp(a)) - pi/2)
    long = mapLngLeft+x/mapWidth*mapLngDelta

    return lat, long


def getWidthHeight():
    """Returns width, height of computer in pixels"""
    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height


def getMap(lat, long, z, driver):
    """Takes in a x and y coordinate as well as the z factor, then gets a map"""

    driver.get("https://www.google.com/maps/@" + str(lat) + "," + str(long) + "," + str(z) + "z")
    driver.fullscreen_window()

    # Removes all of unnessecary icons / buttons on screen

    removeIcon("/html/body/div[3]/div[9]/div[23]/div[5]/div/div[2]", By.XPATH, 'style', "margin-bottom: -200px", driver) # Moves button on bottom left (that changes the type of map one is looking at) downwards out of sight

    # Gets rid of popUps by clicking menu button, then closing it
    wait("/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[1]/button", By.XPATH, # Menu button
    "/html/body/div[3]/div[9]/div[25]/div/div[2]/ul/div[2]/button", By.XPATH, # Close menu button
    driver)

    # Same thing as before, but swapped order
    wait("/html/body/div[3]/div[9]/div[25]/div/div[2]/ul/div[2]/button", By.XPATH, # Close menu button
    "/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[1]/button", By.XPATH, # Menu button
    driver)

    if (z > 7): # If z > 7, then the "groceries, takeout, etc." icons show up
        removeIcon("/html/body/div[3]/div[9]/div[5]/div/div/div", By.XPATH, 'style', "width: 0%", driver)

    # Now map is setup, take screen shot and return
    png = driver.get_screenshot_as_png() # Gets bytes of current screen
    image = Image.open(BytesIO(png)) # Translates those bytes to an Image which we can modify  

    # MAYBE INCLUDE WAIT? ----------------------------------------------
    return image


def wait(buttonPath, findx, resultPath, findy, driver):
    """First input is the button to be clicked, the second is the resultant part that is supposed to show up
    Continuously checks every 500 milliseconds"""
    while True:
        try:
            button = driver.find_element(findx, buttonPath)
            button.click()
        except:
            try:
                driver.find_element(findy, resultPath)
                break
            except:
                pass
        finally:
            sleep(0.5)

def removeIcon(iconPath, findx, nameOfAttribute, value, driver):
    """Sets certain aspects of an icon based on the input parameters so that it disappears. If it fails to find the icon, waits 0.5 seconds
    before trying again"""
    while True:
        try:
            element = driver.find_element(findx, iconPath)
            break
        except:
            sleep(0.5)
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", element, nameOfAttribute, value)


# driver = setUpDriver()
# Sample calls
# map(["859 Barron Ave, Palo Alto", "1095 McGregor Way, Palo Alto", "980 Matadero Ave, Palo Alto", "4029 Arbol Dr, Palo Alto"], "4_places_test.png", driver)

# map(["859 Barron Ave, Palo Alto"], "1_place_test.png", driver)

# map(["64 Action St, Daly City", "58 Action St, Daly City"], "2_really_close_test.png", driver)

# map(["64 Action St, Daly City", "58 Action St, Daly City", "6063 Mission St, Daly City"], "place_covered_by_text_test.png", driver)

# ALWAYS QUIT DRIVER AT THE END TO CLOSE IT
# driver.quit()

