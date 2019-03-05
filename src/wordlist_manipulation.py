#!usr/bin/python
#-*- coding: utf-8 -*-
from standard_functions import *
import re
import datetime

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

def colorWord(word, color):
    # Gives a word a nice color!
    default_color = bcolors.OKBLUE
    return Colors[color] + word + default_color

class signs:
    PLUS = bcolors.OKBLUE + "[" + bcolors.HEADER + "+" + bcolors.OKBLUE + "]" # [+]
    STAR = bcolors.OKBLUE + "[" + bcolors.HEADER + "*" + bcolors.OKBLUE + "]" # [*]
    HELP = bcolors.OKBLUE + "[" + bcolors.HEADER + "h" + bcolors.OKBLUE + "]" # [h]
    INFO = bcolors.OKBLUE + "[" + bcolors.HEADER + "i" + bcolors.OKBLUE + "]" # [i]

class WordlistManipulator:
    #Class with methods for manipulating wordlists and writing them to files.

    def __init__(self, keywords, is_url):
        # Variable for storing the raw keywords
        # These are usefull for manipulation methods that don't need to manipulate
        # the entire wordlist, but work based on keywords (like wordCloner).
        self.keywords = keywords
        self.used_url = is_url
        # Maximum number to be added to each keyword
        self.number_lengths = {"simple" : 100, "normal" : 150, "advanced": 200}
        # Holds the current year.
        self.cur_year = datetime.datetime.now().year

    def fillWordlist(self):
        # Fills the wordlist with our keywords.
        wordlist = []
        for x in range(0, len(self.keywords)):
            wordlist.append(self.keywords[x])
        return wordlist

    def simpleManipulation(self):
        # Called when simple mode is used
        wordlist = self.fillWordlist()
        wordlist = self.addSpecialChars(wordlist, "simple", affixes="src/affixes")
        wordlist = self.capitalizeWord(wordlist)
        wordlist = self.wordCloner(wordlist, "simple")
        wordlist = self.appendYears(wordlist, "simple", self.number_lengths["simple"])
        wordlist = self.leetify(wordlist, "simple")
        wordlist = self.sortOnLength(wordlist)
        self.writeWordlist(wordlist, "simple")

    def normalManipulation(self):
        # Called when normal mode is used
        wordlist = self.fillWordlist()
        wordlist = self.addSpecialChars(wordlist, "normal", affixes="src/affixes")
        wordlist = self.capitalizeWord(wordlist)
        wordlist = self.wordCloner(wordlist, "normal")
        wordlist = self.leetify(wordlist, "normal")
        wordlist = self.appendYears(wordlist, "normal", self.number_lengths["normal"])
        wordlist = self.sortOnLength(wordlist)
        self.writeWordlist(wordlist, "normal")

    def advancedManipulation(self):
        # Called when advanced mode is used
        wordlist = self.fillWordlist()
        wordlist = self.addSpecialChars(wordlist, "advanced", affixes="src/affixes")
        wordlist = self.capitalizeWord(wordlist)
        wordlist = self.wordCloner(wordlist, "advanced")
        wordlist = self.leetify(wordlist, "advanced")
        wordlist = self.appendYears(wordlist, "advanced", self.number_lengths["advanced"])
        wordlist = self.sortOnLength(wordlist)
        self.writeWordlist(wordlist, "advanced")

    def capitalizeWord(self, wordlist):
        # Makes interesting combinations of uppercase and lowercase letters.
        for w in range(0, len(wordlist)):
            # TODO
            # make first and last LETTER capitalized

            for x in range(0, len(wordlist[w])):
                # Cycles trough the word capatalizing one letter at a time
                tmp = wordlist[w][0:x] + wordlist[w][x].upper() + wordlist[w][x + 1 :]
                wordlist.append(tmp)

            # Capitalize entire word
            wordlist.append(wordlist[w].upper())
        return wordlist

    def addZeroToTen(self, wordlist):
        StandardFunc.dynamicPrint(signs.PLUS + " Adding zero to ten.")
        for x in range(0,len(wordlist)):
            for i in range(0,10):
                wordlist.append(wordlist[x] + str(i))
        return wordlist

    def addSpecialChars(self, wordlist, mode, affixes):
        # Adds special characters to the end and beginning of supplied keywords.
        StandardFunc.dynamicPrint(signs.PLUS + " Adding special characters.")
        suffixes, prefixes = StandardFunc.readFile(affixes)[:2]
        numPrevix = len(prefixes)
        numSuffix = len(suffixes)
        minmax = numPrevix, numSuffix
        minim = min(minmax, key=int)
        for x in range(0,len(wordlist)):
            for j in range(0, numSuffix):
                wordlist.append(wordlist[x] + suffixes[j])
            if not (mode == "simple"):
                for k in range(0, numPrevix):
                    wordlist.append(prefixes[k] + wordlist[x])
            if (mode == "advanced"):
                for h in range(0, minim):
                    wordlist.append(prefixes[h] + wordlist[x] + suffixes[h])
        return wordlist

    def appendYears(self, wordlist, mode , year_range):
        # Appends a year after the keyword
        # Coffee -> Coffee1990
        StandardFunc.dynamicPrint(signs.PLUS + " Adding years.")
        year_min = self.cur_year - year_range
        if not (mode == "advanced"):
            if (mode == "normal"):
                # Also capitalize the first letter if its not already a capital
                # and add the years.
                for x in range(0, len(self.keywords)):
                    if not (self.keywords[x].istitle()):
                        keyword = self.keywords[x].capitalize()
                        for i in range(year_min, self.cur_year):
                            wordlist.append(keyword + str(i))
            for x in range(0, len(self.keywords)):
                for i in range(year_min, self.cur_year):
                    wordlist.append(self.keywords[x] + str(i))
        else :
            # Add the years to every wordlist entry
            for x in range(0, len(wordlist)):
                for i in range(year_min, self.cur_year):
                    wordlist.append(wordlist[x] + str(i))
        return wordlist

    def wordCloner(self, wordlist, mode):
        if (mode == "simple"):
            # Duplicates the keyword only
            # Coffee -> CoffeeCoffee
            StandardFunc.dynamicPrint(signs.PLUS + " Duplicating words.")
            for x in range(0, len(self.keywords)):
                wordlist.append(self.keywords[x] + self.keywords[x])
        elif (mode == "normal" or mode == "advanced"):
            # Duplicates the keyword only if it has no numbers in it
            # Coffee -> CoffeeCoffee, CoFfEe -> CoFfEeCoFfEe
            StandardFunc.dynamicPrint(signs.PLUS + " Duplicating words.")
            for x in range(0, len(self.keywords)):
                if not StandardFunc.hasNumber(self.keywords[x]):
                    wordlist.append(self.keywords[x] + self.keywords[x])
        return wordlist

    def leetify(self, wordlist, mode):
        StandardFunc.dynamicPrint(signs.PLUS + " L33t1fy1ng!")
        for x in range(0,len(wordlist)):
            if not (mode == "simple"):
                word = wordlist[x]
                wordlist.append(word.replace("a","4").replace("e","3").replace("o","0").replace("i","1"))
                upp_leet = word.replace("A","4").replace("E","3").replace("O","0").replace("I","1")
                if not (upp_leet == word):
                    wordlist.append(upp_leet)
            else:
                wordlist.append(wordlist[x].replace("a","@").replace("o","0"))

        return wordlist

    def sortOnLength(self, wordlist):
        # Sorts the wordlist on length
        StandardFunc.dynamicPrint(signs.PLUS + " Sorting words by their length.")
        # Casting to a set removes dupicates
        wordlist = list(set(wordlist))
        # Sorting the wordlist by length
        wordlist = sorted(wordlist, key = len)
        return wordlist

    def writeWordlist(self, wordlist, mode):
        # Writes the wordlist from memory to disk
        if (self.used_url):
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
