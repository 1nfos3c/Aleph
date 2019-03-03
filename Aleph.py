import sys
import os
from time import sleep

# Making sure Python can find the other files
src_path = os.getcwd() + '/src'
sys.path.insert(0, src_path)

from wordlist_manipulation import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

Colors = [bcolors.HEADER,bcolors.OKBLUE,bcolors.OKGREEN,bcolors.WARNING,bcolors.FAIL,bcolors.ENDC,bcolors.BOLD,bcolors.UNDERLINE]

class signs:
	PLUS = bcolors.OKBLUE + "[" + bcolors.HEADER + "+" + bcolors.OKBLUE + "]"
	STAR = bcolors.OKBLUE + "[" + bcolors.HEADER + "*" + bcolors.OKBLUE + "]"
	HELP = bcolors.OKBLUE + "[" + bcolors.HEADER + "h" + bcolors.OKBLUE + "]"
	INFO = bcolors.OKBLUE + "[" + bcolors.HEADER + "i" + bcolors.OKBLUE + "]"

def colorWord(word, color):
	# Gives a word a nice color!
	default_color = bcolors.OKBLUE
	return Colors[color] + word + default_color

def printBanner():
	banner = bcolors.HEADER + """   __    __    ____  ____  _   _ 
  /__\  (  )  ( ___)(  _ \( )_( )
 /(__)\  )(__  )__)  )___/ ) _ ( 
(__)(__)(____)(____)(__)  (_) (_)
"""
	print(banner)

print(signs.STAR + " Welcome to " + colorWord("Aleph",0) + "!\n    The one word wordlist generator.")
printBanner()

def printHelp():
	# Prints out the help info
	print(signs.HELP + " Usage : python {} ".format(colorWord(sys.argv[0], 0))+ "<" + colorWord("keyword", 0)+ "> " + colorWord("--simple", 0) + "/" + colorWord("--normal", 0) + "/" + colorWord("--advanced", 0) ) 


def createWordlist(wordlist, keyword, mode):
	# Creates the wordlist
	number_lengths = {"simple" : 10, "normal" : 75, "advanced": 200}
	wordlist = addSpecialChars(wordlist, keyword)
	wordlist = capitalizeWord(wordlist)
	wordlist = appendNumbers(wordlist, number_lengths[mode])
	wordlist = wordCloner(wordlist, keyword)
	if not (mode == "simple" or mode == "normal"):
		wordlist = leetify(wordlist)
	wordlist = sortOnLength(wordlist)
	writeWordlist(wordlist, mode)

if (len(sys.argv) < 3):
	printHelp()
	exit(0)

keyword = sys.argv[1]
keywrds = keyword.split(',')
if (len(keywrds) > 1):
	print("[+] Please use a different tool..")

wordlist = []
keyword = keyword.replace(" ", "")
print( signs.INFO +" Keyword : " + "{}".format(colorWord(keyword,0)))

if (sys.argv[2] == '--simple'):
	createWordlist(wordlist, keyword, "simple")
elif (sys.argv[2] == '--normal'):
	createWordlist(wordlist, keyword, "normal")
elif (sys.argv[2] == '--advanced'):
	createWordlist(wordlist, keyword, "advanced")
else:
	printHelp()
