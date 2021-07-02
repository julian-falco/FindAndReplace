try:
    # gather inputs
    filePath = input("What is the file path for the folder containing the series?: ")
    seriesName = input("What is the name of the series?: ")
    sectNum = int(input("What is the number of sections in the series? (include the 0 section): "))

    # warn user that the trace files will be rewritten
    input("\nWARNING: This program will edit the trace files and cannot be undone.\n" +
          "Backing up your trace files is recommended.\n" +
          "Press enter to continue or Ctrl+c at any time to exit.\n")

    # ask for what should be searched for and replaced
    find = input("Enter the set of characters you would like to search for: ")
    replace = input("Enter the set of characters you would like to replace it with: ")

    # check if user wants to only replace certain instances of the character set
    print("If you wish to replace all instances of " + find + " with " + replace + ", then enter the number 1 below.")
    print("If you would like to specifically choose what to replace, then enter the number 2 below.")

    replaceAll = input("What would you like to do?: ")
    while replaceAll != "1" and replaceAll != "2":
        replaceAll = input("Please enter a valid answer. (y/n): ")
    print()

    # find everything that matches what is being searched for and print it for the user
    # allow user to select which ones to replace if desired
    toReplace = []
    for i in range(sectNum):

        # read the file into a list
        fileName = filePath + "\\" + seriesName + "." + str(i)
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
    input("\nPress enter to replace all selected instances.")

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
