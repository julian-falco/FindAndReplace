import os
from tkinter import *
from tkinter.filedialog import *

def getSeriesInfo(fileName):
    """Return the series name and number of sections."""

    # get only the name
    seriesName = fileName.replace(".ser", "")
    
    # find out how many sections there are
    sectionNums = []
    
    # search each file in the folder that ends with a number
    for file in os.listdir():
        try:
            sectionNums.append(int(file[file.rfind(".")+1:]))
        except:
            pass

    # sort the section numbers so they are in order
    sectionNums.sort()

    return seriesName, sectionNums

try:
    input("Press enter to open your file explorer and select the series file.")

    # create tkinter object but don't display extra window
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()

    # open file explorer to series file
    fileName = askopenfilename(title="Open a Series File",
                           filetypes=(("Series File", "*.ser"),
                                      ("All Files","*.*")))
    if not fileName:
        raise Exception("No file selected.")

    # get needed series info
    filePath = fileName[:fileName.rfind("/")]
    seriesFile = fileName[fileName.rfind("/"):]
    os.chdir(filePath)
    
    seriesName, sectNums = getSeriesInfo(seriesFile)

    # warn user that the trace files will be rewritten
    input("\nWARNING: This program will edit the trace files and cannot be undone.\n" +
          "Backing up your trace files is recommended." +
          "\nPress enter to continue.")

    # ask for what should be searched for and replaced
    find = input("\nEnter the set of characters you would like to search for: ")
    replace = input("Enter the set of characters you would like to replace it with: ")

    # check if user wants to only replace certain instances of the character set
    print("\nIf you wish to replace all instances of " + find + " with " + replace + ", then enter the number 1 below.")
    print("If you would like to specifically choose what to replace, then enter the number 2 below.")

    replaceAll = input("\nWhat would you like to do? (enter 1 or 2): ")
    while replaceAll != "1" and replaceAll != "2":
        replaceAll = input("Please enter a valid answer. (y/n): ")
    print()

    # find everything that matches what is being searched for and print it for the user
    # allow user to select which ones to replace if desired
    toReplace = []
    for i in sectNums:

        # read the file into a list
        fileName = filePath + "/" + seriesName + "." + str(i)
        sectionFile = open(fileName, "r")
        lines = sectionFile.readlines()
        sectionFile.close()

        for line in lines:
            splitLine = line.split('"')

            # check if there is an object name in line, then check if it contains the desired string in the right place
            if '<Contour name="' in line and find in splitLine[1] and not splitLine[1] in toReplace:
                print(splitLine[1] + " was found.")
                if replaceAll == "2":
                    response = input("Would you like to replace " + find + " with " + replace + "? (y/n): ")
                    while response != "y" and response != "n" and response != "":
                        response = input("Please enter a valid answer (y/n): ")
                    if response == "y":
                        toReplace.append(splitLine[1])
                    print()
                else:
                    toReplace.append(splitLine[1])

    # also read series file for ztrace renaming
    fileName = filePath + "\\" + seriesName + ".ser"
    seriesFile = open(fileName, "r")
    lines = seriesFile.readlines()
    seriesFile.close()

    for line in lines:
        splitLine = line.split('"')

        # check if there is an object name in line, then check if it contains the desired string in the right place
        if '<ZContour name="' in line and find in splitLine[1] and not splitLine[1] in toReplace:
            print(splitLine[1] + " was found.")
            if replaceAll == "2":
                response = input("Would you like to replace " + find + " with " + replace + "? (y/n): ")
                while response != "y" and response != "n" and response != "":
                    response = input("Please enter a valid answer (y/n): ")
                if response == "y":
                    toReplace.append(splitLine[1])
                print()
            else:
                toReplace.append(splitLine[1])
    
    # final confirmation
    input("\nPress enter to confirm replacement of all selected instances.\n" +
          "This CANNOT be undone.")

    # iterate through files, doing replacements
    for i in range(sectNum):
        fileName = filePath + "\\" + seriesName + "." + str(i)
        sectionFile = open(fileName, "r")
        lines = sectionFile.readlines()
        sectionFile.close()

        sectionFile = open(fileName, "w")

        for line in lines:
            splitLine = line.split('"')
            if '<Contour name="' in line and splitLine[1] in toReplace:
                splitLine[1] = splitLine[1].replace(find, replace)
                line = '"'.join(splitLine) + '"'
            sectionFile.write(line)

        sectionFile.close()

    # perform replacements in series file
    fileName = filePath + "\\" + seriesName + ".ser"
    seriesFile = open(fileName, "r")
    lines = seriesFile.readlines()
    seriesFile.close()

    seriesFile = open(fileName, "w")

    for line in lines:
        splitLine = line.split('"')
        if '<ZContour name="' in line and splitLine[1] in toReplace:
            splitLine[1] = splitLine[1].replace(find, replace)
            line = '"'.join(splitLine) + '"'
        seriesFile.write(line)

    seriesFile.close()

    print("\nCompleted successfully!")

except Exception as e:
    print("\nERROR: " + str(e))

input("\nPress enter to exit.")  
