#!usr/bin/python
#-*- coding: utf-8 -*-
from standard_functions import *
import re

#Class for printing in terminal with colors
class bcolors:
    HEADER =    '\033[95m'
    OKBLUE =    '\033[94m'
    OKGREEN =   '\033[92m'
    WARNING =   '\033[93m'
    FAIL =      '\033[91m'
    ENDC =      '\033[0m'
    BOLD =      '\033[1m'
    UNDERLINE = '\033[4m'

Colors = [
	bcolors.HEADER,    # \033[95m
	bcolors.OKBLUE,    # \033[94m
	bcolors.OKGREEN,   # \033[92m
	bcolors.WARNING,   # \033[93m
	bcolors.FAIL,      # \033[91m
	bcolors.ENDC,      # \033[0m
	bcolors.BOLD,      # \033[1m
	bcolors.UNDERLINE, # \033[4m
	]

class signs:
	PLUS = bcolors.OKBLUE + "[" + bcolors.HEADER + "+" + bcolors.OKBLUE + "]" # [+]
	STAR = bcolors.OKBLUE + "[" + bcolors.HEADER + "*" + bcolors.OKBLUE + "]" # [*]
	HELP = bcolors.OKBLUE + "[" + bcolors.HEADER + "h" + bcolors.OKBLUE + "]" # [h]
	INFO = bcolors.OKBLUE + "[" + bcolors.HEADER + "i" + bcolors.OKBLUE + "]" # [i]

def colorWord(word, color):
	# Gives a word a nice color!
	default_color = bcolors.OKBLUE
	return Colors[color] + word + default_color

def capitalizeWord(wordlist):
	# Makes interesting combinations of uppercase and lowercase letters.
	for w in range(0, len(wordlist)):

		# TODO
		# make first and last LETTER capitalized

		# First letter and last letter
		for x in range(0, len(wordlist[w])):
			# One Capital for each position
			tmp = wordlist[w][0:x] + wordlist[w][x].upper() + wordlist[w][x + 1 :]
			wordlist.append(tmp)

		# Capitalize entire word
		wordlist.append(wordlist[w].upper())
	return wordlist

def addZeroToTen(wordlist, keyword):
	StandardFunc.dynamicPrint(signs.PLUS + " Adding zero to ten.")
	wordlist.append(keyword)
	for i in range(0,10):
		wordlist.append(keyword + str(i))
	return wordlist

def addSpecialChars(wordlist, keyword, affixes):
	# Adds special characters to the end and beginning of supplied keywords.
	wordlist = addZeroToTen(wordlist, keyword)
	StandardFunc.dynamicPrint(signs.PLUS + " Adding special characters.")
	suffixes, prefixes = readFile(affixes)[:2]
	numPrevix = len(prefixes)
	numSuffix = len(suffixes)
	minmax = numPrevix, numSuffix
	minim = min(minmax, key=int)
	for x in range(0,len(wordlist)):
		for j in range(0, numSuffix):
			wordlist.append(wordlist[x] + suffixes[j])
		for k in range(0, numPrevix):
			wordlist.append(prefixes[k] + wordlist[x])
		for h in range(0, minim):
			wordlist.append(prefixes[h] + wordlist[x] + suffixes[h])
	return wordlist

def capitalizeList(keylist):
	# Makes interesting combinations of uppercase and lowercase from the keyword.
	# Returns new list of keywords
	base = keylist[0].lower()
	keylist.append(base)
	for x in range(0, len(base)):
		tmp = base[0:x] + base[x].upper() + base[x + 1 :]
		tmp2 = base[0:x].upper() + base[x] + base[x + 1 :].upper()
		keylist.append(tmp)
		keylist.append(tmp2)
	keylist.append(base.upper())
	return keylist

def appendNumbers(wordlist, maxnum):
	# Appends numbers 0->range after keyword
	# Todo : Dont just add numbers, add DDMMYY and YYYY
	StandardFunc.dynamicPrint(signs.PLUS + " Adding numbers.")
	for x in range(0, len(wordlist)):
		for i in range(0, maxnum):
			wordlist.append(wordlist[x] + str(i))
	return wordlist

def wordCloner(wordlist, keyword):
	# Duplicates the keyword only
	StandardFunc.dynamicPrint(signs.PLUS + " Duplicating words.")
	keylist = []
	keylist.append(keyword)
	keylist = capitalizeList(keylist)
	for key in keylist:
		wordlist.append(key + key)
	return wordlist

def leetify(wordlist):
	StandardFunc.dynamicPrint(signs.PLUS + " L33t1fy1ng!")
	for x in range(0,len(wordlist)):
		word = wordlist[x]
		lowLeet = wordlist[x].replace("a","4").replace("e","3").replace("o","0").replace("i","1")
		uppLeet = wordlist[x].replace("A","4").replace("E","3").replace("O","0").replace("I","1")
		if not (lowLeet == word):
			wordlist.append(lowLeet)
		if not (uppLeet == word):
			wordlist.append(uppLeet)
	return wordlist

def sortOnLength(wordlist):
	# Sorts the wordlist on length
	StandardFunc.dynamicPrint(signs.PLUS + " Sorting words by their length.")
	# Casting to a set removes dupicates
	wordlist = list(set(wordlist))
	# Sorting the wordlist by length
	wordlist = sorted(wordlist, key = len)
	return wordlist

def writeWordlist(wordlist, mode):
	# Writes the wordlist from memory to disk
    isurl = re.search(r'https?://', sys.argv[1])
    if (isurl is not None):
        url = "{}-wordlist-{}.txt".format(sys.argv[1],mode)
        filename = re.sub(r'(https?://)', '', url)
        filename = re.sub(r'(/)', '_', filename)
        filename = 'wordlists/' + filename
    else:
        filename = " wordlists/{}-wordlist-{}.txt".format(sys.argv[1],mode)
    filename = filename.replace(" ", "").replace(",","-")
    StandardFunc.dynamicPrint(signs.PLUS + " Writing wordlist to : " +"{}".format(colorWord(filename,0)))
    file = open(filename,'w')
    for x in range(0,len(wordlist)):
        file.write(wordlist[x] + "\n")
    file.close()
    print("\n" + signs.STAR +" Wrote " + "{} ".format(colorWord(str(len(wordlist)),0)) + "words to file.")
    exit(0)
