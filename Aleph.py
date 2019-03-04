#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import os
from time import sleep

# Making sure Python can find the other files
src_path = os.getcwd() + '/src' # Path = Current Directory/src
sys.path.insert(0, src_path)

from wordlist_manipulation import * # Import code from src/wordlist_manipulation.py

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
  # [h] Usage : python Aleph.py <keyword> --simple/--normal/--advanced

def createWordlist(wordlist, keyword, mode):
	# Creates the wordlist
	number_lengths = {"simple" : 10, "normal" : 75, "advanced": 200} # Maximum number of words
	wordlist = addSpecialChars(wordlist, keyword)
	wordlist = capitalizeWord(wordlist)
	wordlist = appendNumbers(wordlist, number_lengths[mode])
	wordlist = wordCloner(wordlist, keyword)
	if not (mode == "simple" or mode == "normal"): # If mode is advanced
		wordlist = leetify(wordlist)
	wordlist = sortOnLength(wordlist)
	writeWordlist(wordlist, mode)

if (len(sys.argv) < 3): # 2 Arguments required, word and mode (script name treated as argument 0)
	printHelp()
	exit(0)

keyword = sys.argv[1]
keywrds = keyword.split(',')
if (len(keywrds) > 1): # Only one word currently supported
	print("[+] Please use a different tool..")
	exit(0)

wordlist = []
keyword = keyword.replace(" ", "")
print( signs.INFO +" Keyword : " + "{}".format(colorWord(keyword,0))) # [i] Keyword : {keyword}

if (sys.argv[2] == '--simple'):
	createWordlist(wordlist, keyword, "simple")
elif (sys.argv[2] == '--normal'):
	createWordlist(wordlist, keyword, "normal")
elif (sys.argv[2] == '--advanced'):
	createWordlist(wordlist, keyword, "advanced")
else:
	printHelp()
