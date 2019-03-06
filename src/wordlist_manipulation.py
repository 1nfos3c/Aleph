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
        self.configuration = StandardFunc.readConfigFile()
        self.keywords = keywords
        string = signs.INFO + " keyword(s) : "
        num_keywords = len(keywords)

        for x in range(0, num_keywords):
            if (x == (num_keywords - 1)):
                string = string + colorWord(self.keywords[x],0)
            else:
                string = string + colorWord(self.keywords[x],0) + ", "

        print(string)

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

    def simpleManipulation(self, do_write):
        # Called when simple mode is used
        wordlist = self.fillWordlist()
        wordlist = self.addZeroToNinetynine(wordlist)
        wordlist = self.addSpecialChars(wordlist, "simple")
        wordlist = self.capitalizeWordlist(wordlist)
        #wordlist = self.leetify(wordlist, "simple")
        wordlist = self.wordCloner(wordlist, "simple")
        wordlist = self.sortOnLength(wordlist)
        if(do_write == True):
            self.writeWordlist(wordlist, "simple")
            return None
        else:
            return wordlist

    def normalManipulation(self, do_write):
        # Called when normal mode is used
        wordlist = self.fillWordlist()
        wordlist = self.addSpecialChars(wordlist, "normal")
        wordlist = self.capitalizeWordlist(wordlist)
        wordlist = self.leetify(wordlist, "normal")
        wordlist = self.appendYears(wordlist, "normal", self.number_lengths["normal"])
        wordlist = self.wordCloner(wordlist, "normal")
        wordlist = self.sortOnLength(wordlist)
        if(do_write == True):
            self.writeWordlist(wordlist, "normal")
            return None
        else:
            return wordlist

    def advancedManipulation(self, do_write):
        # Called when advanced mode is used
        wordlist = self.fillWordlist()
        wordlist = self.addSpecialChars(wordlist, "advanced")
        wordlist = self.capitalizeWordlist(wordlist)
        wordlist = self.leetify(wordlist, "advanced")
        wordlist = self.appendYears(wordlist, "advanced", self.number_lengths["advanced"])
        wordlist = self.wordCloner(wordlist, "advanced")
        wordlist = self.sortOnLength(wordlist)
        if(do_write == True):
            self.writeWordlist(wordlist, "advanced")
            return None
        else:
            return wordlist

    def writeAll(self, wordlists):
        # Writes all created wordlists to a single file.
        self.writeWordlist(wordlists, "all")


    def capitalizeWordlist(self, wordlist):
        # Makes interesting combinations of uppercase and lowercase letters.
        # coffee -> Coffee
        for w in range(0, len(wordlist)):
            # TODO
            # make first and last LETTER capitalized

            for x in range(0, len(wordlist[w])):
                # Cycles trough the word capatalizing one letter at a time
                # coffee -> Coffee -> cOffee -> coFfee
                tmp = wordlist[w][0:x] + wordlist[w][x].upper() + wordlist[w][x + 1 :]
                wordlist.append(tmp)

            # Capitalize entire word
            wordlist.append(wordlist[w].upper())
        return wordlist

    def addZeroToNinetynine(self, wordlist):
        # Adds zero to 99 to the keyword(s)
        # Coffee -> Coffee21
        StandardFunc.dynamicPrint(signs.PLUS + " Adding zero to ten.")

        for x in range(0,len(wordlist)):
            for i in range(0,100):
                wordlist.append(wordlist[x] + str(i))
        return wordlist

    def addSpecialChars(self, wordlist, mode):
        # Adds special characters to the end and beginning of supplied keywords.
        # Coffee -> Coffee_ & ~Coffee & @Coffee!
        StandardFunc.dynamicPrint(signs.PLUS + " Adding special characters.")
        suffixes = self.configuration['suffixes']
        prefixes = self.configuration['prefixes']
        numPrevix = len(prefixes)
        numSuffix = len(suffixes)
        minmax = numPrevix, numSuffix
        minim = min(minmax, key=int)
        for x in range(0,len(wordlist)):
            for j in range(0, numSuffix):
                wordlist.append(wordlist[x] + suffixes[j])
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
            # Also capitalize the first letter if its not already a capital
            # and add the years.

            # We will need to avoid looping the words twice, but we do want
            # to add a capitalized version when needed, watch this.
            new_words_written = 0 # <--- !
            for x in range(0, len(self.keywords)):
                if not (self.keywords[x].istitle()):
                    keyword = self.keywords[x].capitalize()
                    for i in range(year_min, self.cur_year):
                        wordlist.append(keyword + str(i))
                        new_words_written += 1 # <--- !!

            for x in range(0, (len(wordlist) - new_words_written)): # <---- !!!
                for i in range(year_min, self.cur_year):
                    wordlist.append(wordlist[x] + str(i))
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
                new_word = self.keywords[x] + self.keywords[x]
                wordlist.append(new_word)
                wordlist.append(new_word.upper())
        elif (mode == "normal" or mode == "advanced"):
            # Duplicates the wordlist entry only if it has no numbers in it
            # Coffee -> CoffeeCoffee, CoFfEe -> CoFfEeCoFfEe
            StandardFunc.dynamicPrint(signs.PLUS + " Duplicating words.")
            for x in range(0, len(wordlist)):
                if not StandardFunc.hasNumber(wordlist[x]):
                    wordlist.append(wordlist[x] + wordlist[x])
        return wordlist

    def leetify(self, wordlist, mode):
        # 'Leetifies' the all words in the wordlist.
        # Coffee -> C0ff33
        StandardFunc.dynamicPrint(signs.PLUS + " L33t1fy1ng!")
        for x in range(0,len(wordlist)):
            word = wordlist[x]
            wordlist.append(word.replace("a","4").replace("e","3").replace("o","0").replace("i","1"))
            upp_leet = word.replace("A","4").replace("E","3").replace("O","0").replace("I","1")
            if not (upp_leet == word):
                wordlist.append(upp_leet)
            if not (mode == "simple"):
                wordlist.append(wordlist[x].replace("a","@").replace("o","0").replace("i","4").replace("e","3"))

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
