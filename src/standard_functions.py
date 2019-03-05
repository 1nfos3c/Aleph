import sys
import os

ERASE_LINE = '\x1b[2K'

def hasNumber(string):
    # Checks if there are numbers in the given string
    # returns a boolean
    return any(i.isdigit() for i in string)

def clearLine():
    # Clears the current Terminal line
    sys.stdout.write(ERASE_LINE)
    sys.stdout.flush()

def dynamicPrint(string):
    # Prints to the same Terminal line.
	clearLine()
	sys.stdout.write("\r" + string)
	sys.stdout.flush()

def makeDir(dir):
    # Makes a directory
    os.system("mkdir {}".format(""))

def readFile(filename):
	#Read file
	#Return contents as a string
	contents = []
	with open(filename) as file:
		for line in file:
			contents.append(line.strip("\n").strip("prefixes=").strip("suffixes="))
	return contents
