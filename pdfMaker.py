from fpdf import FPDF

def makePDF(data, filename, orderedData):
    # Pdf to print
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
    widthTracker = [0] * len(orderedData)

    # Processing all data
    for row in data:
        column = 0
        for datum in orderedData:
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
    for header in orderedData:
        pdf.cell(widthTracker[column], line_height, header, 1, 0, 'C')
        column += 1
        
    # Reset after creating headers for page
    pdf.set_font("Times", size=10)
    pdf.ln(line_height)

    # Next is all the data points
    maxRows = 33
    rowNumber = 0
    for row in data:

        # Calculate maximum height of cell required
        maxes = [0] * len(widthTracker)
        for column in range(len(widthTracker)):
            tester_y = testerPDF.get_y()
            testerPDF.multi_cell(widthTracker[column], line_height, row[orderedData[column]], 1, 0, 'C')
            maxes[column] = round((testerPDF.get_y() - tester_y) / line_height)

            # Reset so we don't get weird results
            testerPDF.set_y(tester_y)

        maxi = max(maxes)

        # Check that we're not starting a new page because of cell size
        rowNumber += maxi
        if rowNumber > maxRows:
            pdf.ln(line_height * (maxRows - (rowNumber - maxi) + 1)) # how many lines we need to create before teleporting to beginning of second page
            column = 0
            for header in orderedData:
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
            pdf.multi_cell(w=widthTracker[column], h = line_height * maxi / maxes[column], txt=row[orderedData[column]], border=1, align='C')
            total += widthTracker[column]
            pdf.set_xy(pdf.l_margin + total, y)
        pdf.set_xy(pdf.l_margin, y + line_height * maxi)

    pdf.output(filename + ".pdf")
    pdf.close()
    testerPDF.close()