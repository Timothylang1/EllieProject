import tkinter as tk
import csv
from functools import partial
from math import sqrt, ceil
from tkinter.font import BOLD
from fpdf import FPDF
from pyparsing import col

class Firefly():

    def __init__(self):
        self.rootWin = tk.Tk()
        self.rootWin.title("Project Firefly")

        self.label1 = tk.Label(self.rootWin, text = "File pathway",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.label1.grid(row = 0, column = 0, padx = 5, pady = 5)


        self.entry1 = tk.Entry(self.rootWin, font = "Futura 16",
                          relief = tk.RAISED, bd = 2, width = 14)
        self.entry1.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.entry1.bind("<Return>", self.updateFile)

    def go(self):
        self.rootWin.mainloop()

    def updateFile(self, event):
        # First, read file and copy it to help manipulate
        text = self.entry1.get()
        dataIn = open(text, 'r')
        data = csv.DictReader(dataIn)

        # Copy of the data in question to manipulate
        self.data = []
        for row in data:
            self.data.append(row)
        
        self.fieldnames = data.fieldnames

        # Close data table
        dataIn.close()

        # Update widgets

        # Instruction about column
        self.label1["text"] = "Column to select:"

        self.label2 = tk.Label(self.rootWin, text = "Type of comparison: >, =, <",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.label2.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.label3 = tk.Label(self.rootWin, text = "Data to compare:",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.label3.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.successLabel = tk.Label(self.rootWin, text = "Result displayed here",
                          font = "Futura 16 bold", relief = tk.RAISED,
                          bd = 2)
        self.successLabel.grid(row = 3, column = 2, padx = 5, pady = 5)

        # Replace entry with label
        self.entry1.destroy()
        self.column = tk.Label(self.rootWin, text = "",
                          font = "Futura 16", relief = tk.RAISED,
                          bd = 2, width=14, bg="white")
        self.column.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.entryList = []

        self.entry2 = tk.Entry(self.rootWin, font = "Futura 16",
                          relief = tk.RAISED, bd = 2, width = 14, justify="center")
        self.entry2.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.entryList.append(self.entry2)

        self.entry3 = tk.Entry(self.rootWin, font = "Futura 16",
                          relief = tk.RAISED, bd = 2, width = 14, justify="center")
        self.entry3.grid(row = 2, column = 1, padx = 5, pady = 5)
        self.entryList.append(self.entry3)

        self.buttonList = []

        self.enterButton = tk.Button(self.rootWin, font = "Futura 16", text="Eliminate data that \n doesn't fit the parameters",
                          relief = tk.RAISED, bd = 2, command=self.selectData)
        self.enterButton.grid(row = 3, column = 1, padx = 5, pady = 5)
        self.buttonList.append(self.enterButton)

        self.deleteButton = tk.Button(self.rootWin, font = "Futura 16", text="Delete column",
                          relief = tk.RAISED, bd = 2, command=self.deleteData)
        self.deleteButton.grid(row = 0, column = 2, padx = 5, pady = 5)
        self.buttonList.append(self.deleteButton)

        self.printButton = tk.Button(self.rootWin, font = "Futura 16", text="Print current data",
                          relief = tk.RAISED, bd = 2, command=self.printData)
        self.printButton.grid(row = 3, column = 0, padx = 5, pady = 5)
        self.buttonList.append(self.printButton)

        toplevel = tk.Toplevel()
        toplevel.title("Headers in file")
        toplevel.protocol("WM_DELETE_WINDOW", self.nothing)
        tracker = 0
        squareShape = round(sqrt(float(len(self.fieldnames))))
        for field in self.fieldnames:
            button = tk.Button(toplevel, font = "Futura 10", text=field,
                          relief = tk.RAISED, bd = 2, command=partial(self.updateColumnLabel, field))
            button.grid(row = tracker // squareShape, column = (tracker + squareShape) % squareShape, padx = 5, pady = 5)
            self.buttonList.append(button)
            tracker += 1
    
    def nothing(self):
        # Used for cancelling closing the toplevels because if the toplevels close, then the whole application fails
        pass

    def updateColumnLabel(self, field):
        self.column["text"] = field
        
    def selectData(self):
        self.disableButtons()
        # Continue selecting data
        column = self.column["text"]
        toCompare = self.entry3.get()
        typeOfComparison = self.entry2.get()
        if typeOfComparison == "=":
            toCompare = toCompare.split(",")            
            self.data = list(filter(lambda row: row[column] in toCompare, self.data))
            self.successLabel["text"] = "Removed all elements \n not equal to " + str(toCompare)
        else:
            try:
                # Test case first
                float(self.data[0][column])
                limit = float(toCompare)

                # Then actual
                if typeOfComparison == ">":
                    self.data = list(filter(lambda row: float(row[column]) > limit, self.data))
                    self.successLabel["text"] = "Removed all elements \n less than " + toCompare

                elif typeOfComparison == "<":
                    self.data = list(filter(lambda row: float(row[column]) < limit, self.data))
                    self.successLabel["text"] = "Removed all elements \n greater than " + toCompare
                
                else:
                    self.successLabel["text"] = "Operation not included in program"

            except ValueError:
                self.successLabel["text"] = "Cannot do operation \n on this column"

            except KeyError:
                self.successLabel["text"] = "Key doesn't exist"
            
        self.enableButtons()

    def deleteData(self):
        self.disableButtons()
        self.deleteButton["text"] = "Processing..."
        toRemove = self.column["text"]
        if toRemove not in self.fieldnames:
            self.successLabel["text"] = "No such header"
        else:
            for row in self.data:
                row.pop(toRemove)
            self.fieldnames.remove(toRemove)

            # ELIMINATES ALL BUTTONS WITH THIS NAME (MIGHT HAVE CONFLICT IF MULTIPLE BUTTONS HAVE THE SAME NAME)
            for button in self.buttonList:
                if button["text"] == toRemove:
                    button.destroy()
                    self.buttonList.remove(button)
                    break
            
            self.successLabel["text"] = "Successfully deleted \n" + toRemove + " column"
        
        self.deleteButton["text"] = "Press to delete column"
        self.enableButtons()

    def printData(self):
        self.disableButtons()
        toplevel = tk.Toplevel()
        toplevel.title("Print Format")
        toplevel.protocol("WM_DELETE_WINDOW", self.nothing)
        tracker = 0
        squareShape = round(sqrt(float(len(self.fieldnames))))
        self.printDataButtons = []
        for field in self.fieldnames:
            button = tk.Button(toplevel, font = "Futura 10", text=field,
                          relief = tk.RAISED, bd = 2, command=partial(self.order, tracker))
            button.grid(row = tracker // squareShape, column = (tracker + squareShape) % squareShape, padx = 5, pady = 5)
            self.printDataButtons.append(button)
            tracker += 1

        instructions = tk.Label(toplevel, font = "Futura 10", text="Click in the order \n you want the columns",
                          relief = tk.RAISED, bd = 2)
        instructions.grid(row = 0, column = squareShape + 1, padx = 5, pady = 5)

        ok = tk.Button(toplevel, font = "Futura 12 bold", text="Enter PDF name below \n then click here to create",
                          relief = tk.RAISED, bd = 2, command=partial(self.finish, toplevel))
        ok.grid(row = 1, column = squareShape + 1, padx = 5, pady = 5)

        self.nameEntry = tk.Entry(toplevel, font = "Futura 12",
                          relief = tk.RAISED, bd = 2, width = 14, justify="center")
        self.nameEntry.grid(row = 2, column = squareShape + 1, padx = 5, pady = 5)

        exit = tk.Button(toplevel, font = "Futura 12 bold", text="Exit",
                          relief = tk.RAISED, bd = 2, command=partial(self.destroy, toplevel))
        exit.grid(row = 3, column = squareShape + 1, padx = 5, pady = 5)

        self.orderedData = []
        self.orderedTracker = 0

    def destroy(self, toplevel):
        toplevel.destroy()
        self.enableButtons()

    def finish(self, toplevel):
        pdf = FPDF('L')
        pdf.add_page()

        pdf.set_font("Times", "B", size=10)
        line_height = pdf.font_size * 1.5

        # The sole purpose of testerPDF is to find the height of multicell blocks based on the text input. This is to determine the height of the text blocks for a more cleaner look
        testerPDF = FPDF()
        testerPDF.add_page()
        testerPDF.set_font("Times", size=10)

        # Calculate nessecary cell width
        # Setup
        widthTracker = [0] * len(self.orderedData)

        # Processing all data
        for row in self.data:
            column = 0
            for datum in self.orderedData:
                widthTracker[column] = len(row[datum])
                column += 1
        
        # Averaging and calculating values
        tol_width = pdf.w - 22
        total = sum(widthTracker)
        for column in range(len(widthTracker)):
            widthTracker[column] = widthTracker[column] * tol_width / total

        # Set up of initial headers:
        pdf.set_font("Times", size=12, style="B")
        column = 0
        for header in self.orderedData:
            pdf.cell(widthTracker[column], line_height, header, 1, 0, 'C')
            column += 1
        
        # Reset after creating headers for page
        pdf.set_font("Times", size=10)
        pdf.ln(line_height)

        # Next is all the data points
        maxRows = 33
        rowNumber = 0
        for row in self.data:

            # Calculate maximum height of cell required
            maxes = [0] * len(widthTracker)
            for column in range(len(widthTracker)):
                tester_y = testerPDF.get_y()
                testerPDF.multi_cell(widthTracker[column], line_height, row[self.orderedData[column]], 1, 0, 'C')
                maxes[column] = round((testerPDF.get_y() - tester_y) / line_height)

                # Reset so we don't get weird results
                testerPDF.set_y(tester_y)

            maxi = max(maxes)

            # Check that we're not starting a new page because of cell size
            rowNumber += maxi
            if rowNumber > maxRows:
                pdf.ln(line_height * (maxRows - (rowNumber - maxi) + 1)) # how many lines we need to create before teleporting to beginning of second page
                column = 0
                for header in self.orderedData:
                    pdf.set_font("Times", size=12, style="B")
                    pdf.cell(widthTracker[column], line_height, header, 1, 0, 'C')
                    column += 1

                # Reset after creating title for page
                pdf.set_font("Times", size=10)
                pdf.ln(line_height)
                rowNumber = maxi # Where we want rowNumber to start on for the next page depends on how big the overlap cells are between the pages
            
            # Adjust all cells for cleaner look based on max height
            y = pdf.get_y()
            total = 0
            for column in range(len(widthTracker)):
                pdf.multi_cell(w=widthTracker[column], h = line_height * maxi / maxes[column], txt=row[self.orderedData[column]], border=1, align='C')
                total += widthTracker[column]
                pdf.set_xy(pdf.l_margin + total, y)
            pdf.set_xy(pdf.l_margin, y + line_height * maxi)

        pdf.output(self.nameEntry.get() + ".pdf")

        self.destroy(toplevel)

        
    def order(self, buttonNum):
        button = self.printDataButtons[buttonNum]
        self.orderedData.append(button["text"])
        button["bg"] = "red"
        button["text"] = str(self.orderedTracker + 1) + " " + button["text"]
        button["font"] = "Futura 10 bold"
        button["state"] = "disabled"
        self.orderedTracker += 1

    def disableButtons(self):
        for button in self.buttonList:
            button["state"] = "disabled"
    
    def enableButtons(self):
        for entry in self.entryList:
            entry.delete(0, 'end')

        self.column["text"] = ""

        for button in self.buttonList:
            button["state"] = "normal"
        
    
rgb = Firefly()
rgb.go()


# C:\Users\bblah\OneDrive\Desktop\1.csv