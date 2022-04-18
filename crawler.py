from numpy import square
import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import time
import tkinter as tk
from math import sqrt
from functools import partial


class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, *args, **kwargs):
        self.myurls = kwargs.get('myurls')
        self.lat = kwargs.get('lat')
        self.long = kwargs.get('long')
        self.display = kwargs.get('display')
        super(MySpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        startTime = time.time()
        for i in range(len(self.myurls)):
            request = scrapy.Request("https://www.google.com/maps/search/" + self.myurls[i].replace(" ", "+"), dont_filter = True, callback=self.parse)
            request.cb_kwargs['placement'] = i # Place for the long or lat to be inserted into the list
            time.sleep(0.4) # Delay between scrape requests so we don't get 429 error

            # Then calculates time remaining + updates labels
            percentageComplete = round(i * 100.0 / len(self.myurls), 2)
            totalElapsedTime = time.time() - startTime
            minutesLeft = round((totalElapsedTime / (i + 1)) * (len(self.myurls) - (i + 1)) / 60) # Total time remaining before completion (in minutes)

            self.display.setText(str(percentageComplete) + "% Complete", "Total time remaining (minutes): " + str(minutesLeft)) # Rounds to two decimal places and updates display
            yield request


    def parse(self, response, placement):
        data = response.text

        # print("THIS IS DATA" + data)
        initialCoor = data.find("center=") + 7
        middlePlace = data.find("%2C", initialCoor)
        endPlace = data.find("&amp", middlePlace)

        try:
            self.lat[placement] = float(data[initialCoor : middlePlace]) # If it can't be converted to a float, then the address simply doesn't exist
            self.long[placement] = float(data[middlePlace + 3 : endPlace])
        except:
            print("Couldn't find address: " + str(placement))



def getLatLongCSV(data, headers, filepath, fieldnames, display):
    """Takes in a filepath for a csv file and a list of headers in order that will assemble the addresses and modifies 
    the csv file to include two new headers, LAT = latitudes, LONG = longitude. Also takes in the tkinter display to update the 
    progress bar directly on it."""
    addresses = listOfAddresses(data, headers) # List of complete addresses to iterate through as well as the original DataFrame from the csv file

    latList = [0.0] * len(addresses) # List of latitudes in order of addresses (default set to 0.0 as a float)
    longList = [0.0] * len(addresses) # List of longitudes

    process = CrawlerProcess()
    process.crawl(MySpider, 
    myurls = addresses,
    lat = latList,
    long = longList,
    display = display)

    process.start()

    # Adds in the new data into the csv data
    for row in range(len(data)):
        data[row]["LAT"] = latList[row]
        data[row]["LONG"] = longList[row]

    # Convert fieldnames from a Sequence (from csv.DICTREADER) to a list
    fieldnamesAsList = []
    for item in fieldnames:
        fieldnamesAsList.append(item)

    fieldnamesAsList.append("LAT")
    fieldnamesAsList.append("LONG")

    # Saves the data into a csv file
    with open(filepath, 'w', newline='') as csvfile: # The newline is to prevent there being a newline inbetween each row of data
        writer = csv.DictWriter(csvfile, fieldnames=fieldnamesAsList)
        writer.writeheader()
        writer.writerows(data)
        csvfile.close()

    # Updates the display, then destroys it
    display.setText("Finished! Saved to: ", filepath)
    

def listOfAddresses(data, headers):
    """Takes in data, and a list of headers. From there, it take the data from that csv file and adds data from the headers
    to create the complete address. Returns a list of addresses as well as the original data from the csv file"""
    addresses = [] # List of addresses to iterate through

    for rowNum in range(len(data)):
        completeAddress = ""
        for header in headers:
            completeAddress += data[rowNum][header] + " "
        addresses.append(completeAddress[0:len(completeAddress) - 1]) # Reason for -1 is to remove the last space from the address
    return addresses


class CreateLATLONGCSVFile():

    def __init__(self, data, fieldnames, filepath, rootWin, mainClass):
        self.rootWin = rootWin
        self.data = data
        self.filepath = filepath
        self.orderedData = []
        self.fieldnames = fieldnames
        self.allLabels = []
        self.mainClass = mainClass

        tracker = 0
        squareShape = round(sqrt(float(len(self.fieldnames))))
        for field in self.fieldnames:
            button = tk.Button(self.rootWin, font = "Futura 10", text=field, relief = tk.RAISED, bd = 2)
            button["command"] = partial(self.order, button)
            button.grid(row = tracker // squareShape, column = (tracker + squareShape) % squareShape, padx = 5, pady = 5)
            tracker += 1
            self.allLabels.append(button)

        self.instructions= tk.Button(self.rootWin, text = """
            WARNING: your CSV file doesn't include latitude or longitude coordinates. \n
            If you WANT to use the map function, please follow the instructions below. If not, click exit to return to mainWindow OR... \n
            If you have custom personal LAT LONG columns in csv file, then click exit to return to mainWindow. \n
            1. Please click headers in order of forming the address \n
            (ex. click header titled address, followed by city, followed by state...) \n
            2. Then CLICK HERE to modify csv input file. \n
            This will override the input csv file to include the new columns of data with the title LAT and LONG \n
            PLEASE READ: this takes time to get all the info. \n
            Last note: if it can't find the address, default is 0.0, 0.0 LAT, LONG""",
            font = "Futura 12", relief = tk.RAISED, bd = 2, command=self.startProcessingData)
        self.instructions.grid(row = squareShape + 1, column = 0, columnspan = squareShape, padx = 5, pady = 5)
        self.allLabels.append(self.instructions)

        exit = tk.Button(self.rootWin, text="EXIT", command=self.destroy, font="Futura 36 bold")
        exit.grid(row = squareShape + 1, column = squareShape + 1)
        self.allLabels.append(exit)

    def destroy(self):
        """Destroys all of the labels of the main window and reverts back to the main program"""
        for widget in self.allLabels:
            widget.destroy()

        self.mainClass.updateFile() # Gives control back to the main class

    def startProcessingData(self):
        """Begins the reactor to start getting LAT LONG of data"""
        # Starts by checking that the user has given any headers
        if len(self.orderedData) == 0:
            self.instructions["text"] = """
            WARNING: your CSV file doesn't include latitude or longitude coordinates. \n
            If you want to use the map function, please follow the instructions below. If not, close this window. \n
            1. PLEASE CLICK HEADERS IN ORDER OF FORMING ADDRESS \n
            (ex. click header titled address, followed by city, followed by state...) \n
            2. Then CLICK HERE to modify csv input file. \n"""
            return

        # Then deletes all of the buttons on the screen
        for widget in self.allLabels:
            widget.destroy()

        # Setsup label to show what percentage is done
        self.progressBar = tk.Label(self.rootWin, text="Setting up reactor...", font = "Futura 12", relief = tk.RAISED, bd = 2)
        self.progressBar.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.minutesLeft = tk.Label(self.rootWin, text="DO NOT CLOSE WINDOW DURING PROCESS", font = "Futura 12", relief = tk.RAISED, bd = 2)
        self.minutesLeft.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.rootWin.update() # Updates the display to reflect the change in the label

        # Starts process
        getLatLongCSV(self.data, self.orderedData, self.filepath, self.fieldnames, self)


    def setText(self, string1, string2):
        """Sets the text on the progress bar to show progress."""
        self.progressBar["text"] = string1
        self.minutesLeft["text"] = string2
        self.rootWin.update()


    def order(self, button):
        self.orderedData.append(button["text"])
        button["bg"] = "red"
        button["text"] = str(len(self.orderedData)) + " " + button["text"]
        button["font"] = "Futura 10 bold"
        button["state"] = "disabled"


    def go(self):
        self.rootWin.mainloop()


def setUp(data, fieldnames, filepath, rootWin, mainClass):
    """Modifies rootWin window that shows current progress towards getting all the LAT / LONG of the data"""
    CreateLATLONGCSVFile(data, fieldnames, filepath, rootWin, mainClass)

# TODO: 
"""1. Fix the update display
2. Figure out how to close the rootWindow seperately between this program and the main program
3. Try to reduce complexity in passing in variables
4. Figure out how to incorporate songs while loading
5. Update time remaining
6. Add new createCSV file button in main window"""