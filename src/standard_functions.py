import sys
import os

ERASE_LINE = '\x1b[2K'

class StandardFunc:
    def hasNumber(string):
        # Checks if there are numbers in the given string
        # returns a boolean
        #this function is not used yet
        return any(i.isdigit() for i in string)

    def clearLine():
        # Clears the current Terminal line
        sys.stdout.write(ERASE_LINE)
        sys.stdout.flush()

    def dynamicPrint(string):
        # Prints to the same Terminal line.
        StandardFunc.clearLine()
        sys.stdout.write("\r" + string)
        sys.stdout.flush()

    def makeDir(dir):
        # Makes a directory
        os.system("mkdir {}".format(""))

    def readConfigFile():
        #Read config file
        #Return configuration as a dict
        configuration = {}
        with open("src/config") as file:
            for line in file:
                configuration[line.strip("\n").split(" ")[0].strip(":")] = line.strip("\n").split(" ")[1]
        return configuration
