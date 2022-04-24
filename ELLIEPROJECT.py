import tkinter as tk
import csv
from functools import partial
from math import sqrt
from tkinter.font import BOLD
import os
from tkinter.filedialog import asksaveasfilename, askopenfilename # Used to save files and open them


# Personal files

import loadMap # Creates map given a list of addresses
import pdfMaker # Creates PDF with any data
import crawler # Used to get lat / long of data for the map
import playSongs # Toplevel used to control songs played # Currently all Glass Animals
import excelMaker # Used to create excel spreadsheets, or add new sheets to existing excel sheets


class Firefly():

    def __init__(self):
        self.rootWin = tk.Tk()
        self.rootWin.title("Project Firefly")

        # Creation of song toplevel
        playSongs.musicMaker(self.rootWin, os.path.join(os.path.dirname(__file__), 'songs'))


        self.label1 = tk.Label(self.rootWin, text = "Welcome to Project Firefly! Please select a csv file to continue...",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.label1.grid(row = 0, column = 0, padx = 5, pady = 5)

        # HISTORY BUTTON MAX IS HERE SINCE WE NEED IT FOR THE INSTRUCTIONS TOP LEVEL
        self.historyButtonMax = 10 # Limits the total number of history buttons

        instructTop = tk.Toplevel()
        instructTop.title("Project FireFly Instructions")
        instructions = tk.Label(instructTop, text=
        """Welcome to Project Firefly! My name is Timothy, and I'm here to guide you through how to use this application (feel free to close this window if you've read this) \n 
        1. First, click the csv file you want to open. \n
        2. After the application has found your file, it will open to a new window. To modify data, click on one of the header buttons in the window titled 'Select Header'. \n
        You will be modifying data in the csv column with that header. Next, choose which operation to use (i.e. equal to, greater than). \n
        Lastly, type in what you want to compare. If the comparison is != or =, you can input multiple items with a COMMA inbetween \n
        \t(ex. State = California, Minnesota will eliminate all rows of data whose state isn't California OR Minnesota). \n
        3. After you have data in all three fields (column, type of comparison, what to compare), click the button in the center. \n
        IMPORTANT: ANY DATA THAT DOESN'T FIT THE GIVEN PARAMETERS WILL BE ELIMINTATED. So, if you want to get rid of all states NOT EQUAL to California \n
        input 'States' for column, '=' for type of comparison, 'California' for what to compare, and it will retain all rows of data whose state is = to California. \n
        4. After modifying data, you can display it using one of the buttons under the label Display Data Types. \n
        5. If you want to undo a comparison, click on one of the history buttons under the window titled 'Last """ + str(self.historyButtonMax) + """ Operations'. Whichever button you click will add in all \n
        the data that was removed from that operation back into the main window. \n
        6. If you have any questions, suggestions, comments, problems, ideas for additional displayed data, or just want to talk about python and how this application was \n
        built from scratch, feel free to text or call me at 650-447-4476.""",
        font="Futura 12", relief = tk.RAISED, bd=2)
        instructions.grid(row=0, column=0, padx = 5, pady = 5)

        self.checkForLatLong(askopenfilename())

    def go(self):
        self.rootWin.mainloop()

    
    def checkForLatLong(self, filepath):
        """Checks if the input csv file contains the LAT LONG header needed for mapping. If not, it offers to override input csv file
        to include the two new columns. The user can still use the input csv file while it's calculating lat/long in the background."""
        # First, read file and copy it to help manipulate
        if len(filepath) == 0: # If no pathway was given, closes application
            self.label1["text"] = "No file given. You just here for the music?"
            return

        if filepath[len(filepath) - 4:len(filepath)] != ".csv": # If the file isn't a csv file
            self.label1["text"] = "Please give a csv file next time. \n Close and reopen application to retry."
            return

        dataIn = open(filepath, 'r')
        data = csv.DictReader(dataIn)

        # Copy of the data in question to manipulate
        self.data = []
        for row in data:
            self.data.append(row)
        
        self.fieldnames = data.fieldnames

        # Close data table
        dataIn.close()

        # Gets rid of all labels at the start
        self.label1.destroy()

        # Then checks if it should add LAT/LONG columns if they don't exist for the map. If it doesn't exist, offer to add it
        if "LAT" not in self.fieldnames or "LONG" not in self.fieldnames:
            crawler.setUp(self.data.copy(), self.fieldnames, filepath, self.rootWin, self) # Takes in the data, the fieldnames, the filepath, the root window, and self to call the self.updateFile() if user has personal LAT LONG columns
        else:
            self.updateFile() # Continues program as normal


    def updateFile(self):
        # Instruction about column
        self.label1 = tk.Label(self.rootWin, text = "Header to Compare:",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.label1.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.label2 = tk.Label(self.rootWin, text = "Type of comparison:\n >, =, <, >=, <=, !=",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.label2.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.label3 = tk.Label(self.rootWin, text = "Data to compare:",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.label3.grid(row = 0, column = 2, padx = 5, pady = 5)

        self.successLabel = tk.Label(self.rootWin, text = "Result displayed here",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.successLabel.grid(row = 2, column = 2, padx = 5, pady = 5)

        # Replace entry with label
        self.column = tk.Label(self.rootWin, text = "",
                          font = "Futura 16", relief = tk.RAISED,
                          bd = 2, width=14, bg="white")
        self.column.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.entryList = []

        self.entry2 = tk.Entry(self.rootWin, font = "Futura 16",
                          relief = tk.RAISED, bd = 2, width = 14, justify="center")
        self.entry2.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.entryList.append(self.entry2)

        self.entry3 = tk.Entry(self.rootWin, font = "Futura 16",
                          relief = tk.RAISED, bd = 2, width = 14, justify="center")
        self.entry3.grid(row = 1, column = 2, padx = 5, pady = 5)
        self.entryList.append(self.entry3)

        # Button list that keeps track of all the buttons to disable and enable when processing data
        self.buttonList = []

        self.enterButton = tk.Button(self.rootWin, font = "Futura 16", text="CLICK HERE \n to modify data",
                          relief = tk.RAISED, bd = 2, command=self.selectData)
        self.enterButton.grid(row = 2, column = 1, padx = 5, pady = 5)
        self.buttonList.append(self.enterButton)

        self.displayTypes = tk.Label(self.rootWin, text = "Display Data Types \n Listed Below:",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.displayTypes.grid(row = 3, column = 0, padx = 5, pady = 5)

        # Each button below creates a toplevel widget and disable all other buttons in other toplevels + main
        # Each toplevel acts the same, the only thing that changes is how the data is displayed
        # So for each, the method of displaying the data is based on the input lambda expression
        # self.displayData(instructions, title of widget, lambda which contains which method to use and the inputs)

        self.printButton = tk.Button(self.rootWin, font = "Futura 16", text="Print current data",
                        relief = tk.RAISED, bd = 2, command=partial(self.displayData, 
                        """1. Click headers above in the order you want the columns \n
                        2. Enter number of entries per pdf on the left (default is size of data set) \n
                        3. Then CLICK HERE to create \n""",
                        "Print Format",
                        lambda A, B, C, D, E, F: createPDF(A, B, C, D, E, F))) # Here is where it distinguishes between which method is used to display data
        self.printButton.grid(row = 4, column = 0, padx = 5, pady = 5)
        self.buttonList.append(self.printButton)


        self.mapButton = tk.Button(self.rootWin, font = "Futura 16", text="Map current data",
                        relief = tk.RAISED, bd = 2, command=partial(self.displayData, 
                        """1. Click LAT header first, then LONG \n
                        2. Enter number of entries per map on the left (default is size of data set) \n
                        3. Then CLICK HERE to create \n
                        PLEASE READ: if this is your first time running this application, it will autoinstall chromedriver \n
                        which takes time. After that, the program will run faster. Please be patient with the first run \n""",
                        "Map Format",
                        lambda A, B, C, D, E, F: createMap(A, B, C, D, E, F)))
        self.mapButton.grid(row = 5, column = 0, padx = 5, pady = 5)
        self.buttonList.append(self.mapButton)

        self.csvButton = tk.Button(self.rootWin, font="Futura 16", text="Create csv",
                        relief = tk.RAISED, bd = 2, command=partial(self.displayData, 
                        """1. Click whichever columns you want in the headers above for the new csv file \n
                        2. Enter number of entries per csv on the left (default is size of data set) \n
                        3. Then CLICK HERE to create \n""",
                        "CSV Format",
                        lambda A, B, C, D, E, F: createCSV(A, B, C, D, E, F)))
        self.csvButton.grid(row = 6, column = 0, padx = 5, pady = 5)
        self.buttonList.append(self.csvButton)

        self.ExcelButton = tk.Button(self.rootWin, font="Futura 16", text="Excel Sheet",
                        relief = tk.RAISED, bd = 2, command=self.createExcel)
        self.ExcelButton.grid(row = 7, column = 0, padx = 5, pady = 5)
        self.buttonList.append(self.ExcelButton)


        # Creates topLevel where each button is a header of the file
        toplevel, buttonlist, squareShape = self.createTopLevel( "Select header", lambda T: self.updateColumnLabel(T))
        self.buttonList.extend(buttonlist) # Adds all the buttons to the main buttons list so that they can be disabled when nessecary


        # History toplevel that saves the last 10 changes to the file you made (starts empty)
        self.history = tk.Toplevel()
        self.historyButtonList = [] # Tracker for all buttons added to history widget
        self.history.title("Last " + str(self.historyButtonMax) + " Operations")
        self.history.protocol("WM_DELETE_WINDOW", self.nothing)
        self.historyInstructions = tk.Label(self.history, text = "Click on any button below \n to add data back in", # Label with instructions
                          font = "Futura 16", relief = tk.RAISED,
                          bd = 2, bg="white")
        self.historyInstructions.grid(row = 0, padx = 5, pady = 5)
        

    def nothing(self):
        # Used for cancelling closing the toplevels because if the toplevels close, then the whole application fails
        pass

    def updateColumnLabel(self, button):
        self.column["text"] = button["text"] # Updates the column label to whatever data the button clicked held
        
    def selectData(self):
        self.disableButtons()
        # Continue selecting data
        column = self.column["text"]
        toCompare = self.entry3.get()
        typeOfComparison = self.entry2.get()
        if typeOfComparison == "=":
            toCompare = self.stringToList(toCompare)
            self.manipulateData(lambda x, y: True if x not in y else False, column, toCompare, "is not equal to")

        elif typeOfComparison == "!=":
            toCompare = self.stringToList(toCompare)        
            self.manipulateData(lambda x, y: True if x in y else False, column, toCompare, "is equal to")        

        else:
            try:
                # Test case first
                float(self.data[0][column])
                toCompareFloat = float(toCompare)

                # Then actual
                if typeOfComparison == ">":
                    self.manipulateData(lambda x, y: True if float(x) <= y else False, column, toCompareFloat, "is less than or equal to")        

                elif typeOfComparison == "<":
                    self.manipulateData(lambda x, y: True if float(x) >= y else False, column, toCompareFloat, "is greater than or equal to")        

                elif typeOfComparison == ">=":
                    self.manipulateData(lambda x, y: True if float(x) < y else False, column, toCompareFloat, "is less than")        

                elif typeOfComparison == "<=":
                    self.manipulateData(lambda x, y: True if float(x) > y else False, column, toCompareFloat, "is greater than")        

                else:
                    self.successLabel["text"] = "Operation not included in program"

            except ValueError:
                self.successLabel["text"] = "Cannot do operation \n on this column"

            except KeyError:
                self.successLabel["text"] = "Key doesn't exist"
            
        self.enableButtons()


    def stringToList(self, string1):
        """Takes in a string (the users input) and turns it into a list"""
        list1 = string1.split(",")
        for i in range(len(list1)):
            list1[i] = list1[i].strip()
        return list1


    def manipulateData(self, expression, column, toCompare, resultsString):
        """Given a lambda expression, uses it to sort and remove data with the column and the data to compareTo. It then updates the results
        label and adds a history button with the data that has been removed"""
        remove = []
        tracker = 0
        while tracker < len(self.data):
            if expression(self.data[tracker][column], toCompare):
                remove.append(self.data[tracker])
                self.data.pop(tracker)
                tracker -= 1
            tracker += 1      
        text = str(len(remove)) + " items whose " + column + "\n " + resultsString + " " + str(toCompare)
        self.successLabel["text"] = "Removed " + text
        self.addHistoryButton(remove, text)


    def addHistoryButton(self, data, text):
        """Adds button to history that when clicked, restores all the data that was removed during a particular operation back to the main list.
        If there are more than 10 history buttons, we remove the last history button"""
        if len(self.historyButtonList) == self.historyButtonMax:
            self.removeButtonFromHistory(self.historyButtonList[0])

        button = tk.Button(self.history, font = "Futura 10", text="Add " + text,
                          relief = tk.RAISED, bd = 2, width=30)
        button["command"] = partial(self.addData, data, button)
        button.grid(row = self.historyButtonMax - len(self.historyButtonList), padx = 5, pady = 5)
        self.buttonList.append(button)
        self.historyButtonList.append(button)


    def addData(self, dataToAdd, button):
        """Readds in data back to the main data list, then deletes button"""
        for item in dataToAdd:
            self.data.append(item)

        # Removes button, then reGrids other buttons below it so that new history buttons added still maintain order
        self.removeButtonFromHistory(button)


    def removeButtonFromHistory(self, button):
        """Removes button from history as well as regridding any buttons below it to retain the order"""
        self.disableButtons()
        self.buttonList.remove(button)

        # Removes button, then regrids previous buttons
        self.historyButtonList.remove(button)
        for i in range(0, len(self.historyButtonList)):
            self.historyButtonList[i].grid(row = self.historyButtonMax - i, padx = 5, pady = 5)
        
        self.successLabel["text"] = button["text"]
        button.destroy()
        self.enableButtons()


    def displayData(self, instructions, title, expression):
        """Takes in instructions (String), name of the top level (String) and a lambda expression that will determine how to display 
        the data (essentially, which method to use)."""
        # First disables all buttons, then creates toplevel
        self.disableButtons()

        toplevel, buttonlist, squareShape = self.createTopLevel(title, lambda T: self.order(T))

        self.ok = tk.Button(toplevel, font = "Futura 12 bold", text=instructions,
                        relief = tk.RAISED, bd = 2, command=partial(self.createDisplay, toplevel, expression))
        self.ok.grid(row = squareShape + 1, column = 0, columnspan = squareShape, padx = 5, pady = 5)

        self.entriesPerSet = tk.Entry(toplevel, font = "Futura 12",
                          relief = tk.RAISED, bd = 2, width = 14, justify="center")
        self.entriesPerSet.insert(0, str(len(self.data)))
        self.entriesPerSet.grid(row = squareShape + 2, column=0, padx = 5, pady = 5)

        exit = tk.Button(toplevel, font = "Futura 12 bold", text="Exit back to main menu",
                          relief = tk.RAISED, bd = 2, command=partial(self.destroy, toplevel))
        exit.grid(row = 0, column = squareShape + 1, padx = 5, pady = 5)

        self.orderedData = []

        return toplevel, squareShape # Return these two items in case we need to slightly modify it


    def destroy(self, toplevel):
        toplevel.destroy()
        self.enableButtons()


    def createDisplay(self, toplevel, expression):
        """Takes in a topLevel widget and a lambda expression which method to use for displaying the data. Before displaying,
        checks to ensure that inputs are all correct"""
        # Checks that user has inputted data correctly
        if len(self.orderedData) == 0:
            self.ok["text"] = "Click header buttons above in the order you want"
            return

        try:
            # Gets data from entries
            entriesPerDisplay = int(self.entriesPerSet.get())
            if entriesPerDisplay > len(self.data):
                self.ok["text"] = "Please enter in number less than \n or equal to the total data set \n Total data set length: " + str(len(self.data))
                return
        except:
            self.ok["text"] = "Please enter valid number in bottom right box"
            return

        # Gets data from toplevel first
        filename = asksaveasfilename(confirmoverwrite=False)
        if len(filename) == 0: # If they didn't pick anything...
            return
        
        # Then destroys topLevel widget, then updates text 
        toplevel.destroy()

        # The last diaplay might not have exactly the number of entries, so we have to ensure that the last display is taken care of
        finalEntryLength = len(self.data) % entriesPerDisplay

        # Total number of displayed data to create NOT INCLUDING THE LAST ONE
        totalNumOfDisplays = (len(self.data) - finalEntryLength) // entriesPerDisplay

        # Based on expression will determine which method is used to display the data (see final methods at the bottom for example) 
        expression(self.data, filename, self.orderedData, totalNumOfDisplays, finalEntryLength, entriesPerDisplay)


    def createTopLevel(self, header, expression):
        """Creates standard toplevel with header, and a button for each column in the csv file.
        Returns: toplevel itself, list of buttons created, and squareShape (i.e. how big of a grid the buttons take)
        Parameters:
        header (String): name of topLevel widget
        expression (lambda): which method to call when one of the column buttons is clicked
        addToButtonList (boolean): if true, adds to overall button list. The list is used to disable all buttons on the screen
        """
        toplevel = tk.Toplevel()
        toplevel.minsize(200, 100)
        toplevel.title(header)
        toplevel.protocol("WM_DELETE_WINDOW", self.nothing)
        tracker = 0
        squareShape = round(sqrt(float(len(self.fieldnames))))
        buttonList = []
        for field in self.fieldnames:
            button = tk.Button(toplevel, font = "Futura 10", text=field,
                          relief = tk.RAISED, bd = 2)
            button["command"] = partial(expression, button)
            button.grid(row = tracker // squareShape, column = (tracker + squareShape) % squareShape, padx = 5, pady = 5)
            buttonList.append(button)
            tracker += 1
        return toplevel, buttonList, squareShape
        

    def order(self, button):
        self.orderedData.append(button["text"])
        button["bg"] = "red"
        button["text"] = str(len(self.orderedData)) + " " + button["text"]
        button["font"] = "Futura 10 bold"
        button["state"] = "disabled"


    def disableButtons(self):
        for button in self.buttonList:
            button["state"] = "disabled"
    

    def enableButtons(self):
        for entry in self.entryList:
            entry.delete(0, 'end') # Clears all entries in main window

        self.column["text"] = ""

        for button in self.buttonList:
            button["state"] = "normal"


    # EXCLUSIVE EXCEL SECTION
    def createExcel(self):
        """Sets up special toplevel for creating excel spreadsheets."""
        toplevel, squareShape = self.displayData("""
                        1. Click headers above in the order you want the columns \n
                        2. Enter title of sheet on the right \n
                        3. Then CLICK HERE to create a single excel file or add on a sheet to a preexisting excel spreadsheet \n
                        Notes: If you click on an existing excel file, the program will add a new sheet to that file. \n
                        If this is the case, ignore the dialog box that warns about replacing files: your data will not be overwritten. \n
                        In any other case, it will create a new .xlsx file from scratch and save it at the pathway given. \n
                        The program will then color in certain entries based on their frequency in previous sheets. The darker the color, the \n
                        more common a certain entry was in previous sheets in the file. If you would like to disable this option, click \n
                        the bottom right button to 'Disable Color' scheme. \n
                        IMPORTANT: DO NOT HAVE FILE OPEN ON ANY APPLICATION WHEN PROGRAM IS RUNNING OR IT WON'T SAVE!
                        """, "Create Excel", True) # No lambda expression, so put a filler boolean
        
        # Slight change of labels and buttons
        self.entriesPerSet.delete(0, tk.END)
        self.entriesPerSet.insert(0, "New Sheet Title")

        # New disable color scheme button
        self.disableColorsButton = tk.Button(toplevel, font = "Futura 12", text="Disable Color",
                          relief = tk.RAISED, bd = 2, width = 14, justify="center")
        self.disableColorsButton["command"] = self.swap
        self.disableColorsButton.grid(row = squareShape + 2, column=max(squareShape - 1, 1), padx = 5, pady = 5) # The max is to ensure that the entries don't end up collapsing on each other in case there aren't that many headers

        # Redirect where the ok button goes
        self.ok["command"] = partial(self.createExcelSheet, toplevel)


    def swap(self):
        if self.disableColorsButton["text"] == "Disable Color":
            self.disableColorsButton["text"] = "Enable Color"
        else:
            self.disableColorsButton["text"] = "Disable Color"


    def createExcelSheet(self, toplevel):
        """Slightly modified verison from all the other data displays. Same concept, but this time creates excel sheet."""

        if len(self.orderedData) == 0:
            self.ok["text"] = "Click header buttons above in the order you want"
            return

        # Gets data from toplevel first
        sheetName = self.entriesPerSet.get()

        colorScheme = False
        if self.disableColorsButton["text"] == "Disable Color":
            colorScheme = True

        # Then asks for file. Automatically adds the ".xlsx" extension since we know we're only creating one xlsx file
        filename = asksaveasfilename(defaultextension=".xlsx", confirmoverwrite=False)
        if len(filename) == 0:
            self.ok["text"] = "Make sure that you have entered a filename \n in the bottom left box"
            return

        # Then destroys topLevel widget, then updates text 
        toplevel.destroy()

        self.successLabel["text"] = "Creating excel sheet... Please wait"
        self.rootWin.update()

        excelMaker.createExcel(filename, sheetName, self.data, self.orderedData, colorScheme)

        self.successLabel["text"] = "Success! Please wait a moment \n before opening excel file"
        self.enableButtons()
        self.rootWin.update()



# Methods that display data (used in the lambda expressions)
# ALL METHODS have to take in three parameters: the data (list), the filename (string), and the headers that the user wants to use (list), totalNumber of complete displayed data, length of final entry, entries
# The reason for the setup is that we can setup other applications before doing the whole process instead of each times setting up
# a new application (for example: for createMaps, we don't need to create a new driver every time we want to move onto the next map)


# Creating PDF's function
def createPDF(data, filename, orderedColumnNames, totalNumOfFullEntries, finalEntryLength, entriesPerDisplay):
    rgb.successLabel["text"] = "Creating pdfs"
    rgb.rootWin.update() # Updates the text
    for i in range(totalNumOfFullEntries):
        pdfMaker.makePDF(data[i * entriesPerDisplay : (i + 1) * entriesPerDisplay], filename + str(i), orderedColumnNames)
            
    if finalEntryLength != 0: # Creation of the last pdf if nessecary
        pdfMaker.makePDF(data[len(data) - finalEntryLength : len(data)], filename + str(totalNumOfFullEntries), orderedColumnNames)
    rgb.enableButtons()
    rgb.successLabel["text"] = "Success!"


# Creating maps function
def createMap(data, filename, orderedColumnNames, totalNumOfFullEntries, finalEntryLength, entriesPerDisplay):
    rgb.successLabel["text"] = "Setting up chrome driver"
    rgb.rootWin.update() # Updates the text

    driver = loadMap.setUpDriver() # Sets up driver
    rgb.successLabel["text"] = "Finished with setup, now processing map... \n DO NOT TOUCH SCREEN, MAKE SURE MOUSE IS IN LOWER CORNER"
    rgb.rootWin.update() # Updates the text

    for i in range(totalNumOfFullEntries):
        makeMap(data[i * entriesPerDisplay : (i + 1) * entriesPerDisplay], filename + str(i), orderedColumnNames, driver)
            
    if finalEntryLength != 0: # Creation of the last map if nessecary
        makeMap(data[len(data) - finalEntryLength : len(data)], filename + str(totalNumOfFullEntries), orderedColumnNames, driver)

    driver.quit() # Closes driver after finishing
    rgb.enableButtons() # Enables all buttons back once finished
    rgb.successLabel["text"] = "Success!"

# Helper for createMaps
def makeMap(subsetOfdata, filename, orderedColumnNames, driver):
    """OrderedColumnNames should have the LATITUDE first followed by the LONGITUDE"""
    lat = []
    long = []
    # Setup for list of addresses
    for row in subsetOfdata:
        lat.append(float(row[orderedColumnNames[0]]))
        long.append(float(row[orderedColumnNames[1]]))

    loadMap.map(lat, long, filename, driver)


# Creating csv files function
def createCSV(data, filename, orderedColumnNames, totalNumOfFullEntries, finalEntryLength, entriesPerDisplay):
    rgb.successLabel["text"] = "Creating CSV files"
    rgb.rootWin.update() # Updates the text
    # Gets rid of all the data that isn't needed so we only have the correct fieldnames
    data = data.copy()
    for row in data:
        for column in row.copy(): # Copies it so that we can safely iterate through it
            if column not in orderedColumnNames:
                row.pop(column)


    for i in range(totalNumOfFullEntries):
        with open(filename + str(i) + ".csv", 'w', newline='') as csvfile: # The newline is to prevent there being a newline inbetween each row of data
            writer = csv.DictWriter(csvfile, fieldnames=orderedColumnNames)
            writer.writeheader()
            writer.writerows(data[i * entriesPerDisplay : (i + 1) * entriesPerDisplay])
            csvfile.close()            
    if finalEntryLength != 0: # Creation of the last pdf if nessecary
        with open(filename + str(totalNumOfFullEntries) + ".csv", 'w', newline='') as csvfile: # The newline is to prevent there being a newline inbetween each row of data
            writer = csv.DictWriter(csvfile, fieldnames=orderedColumnNames)
            writer.writeheader()
            writer.writerows(data[len(data) - finalEntryLength : len(data)])
            csvfile.close()

    rgb.enableButtons() # Enables all buttons back once finished
    rgb.successLabel["text"] = "Success!"

# Start project
rgb = Firefly()
rgb.go()


# Test file
# C:\Users\bblah\OneDrive\Desktop\1.csv
