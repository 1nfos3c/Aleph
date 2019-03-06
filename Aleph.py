#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import os

# Making sure Python can find the other files
src_path = os.getcwd() + '/src' # Path = Current Directory/src
sys.path.insert(0, src_path)
from web_list_generator import *
from wordlist_manipulation import * # Import code from src/wordlist_manipulation.py
from standard_functions import *
from datamuse_generator import *

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
	print(signs.HELP + " Usage : python {} ".format(colorWord(sys.argv[0], 0))+ "<" + colorWord("keyword", 0)+ "> " + colorWord("  --simple", 0) + "/" + "\n\t\t\t\t\t" + colorWord("--normal", 0) + "/" +  "\n\t\t\t\t\t" + colorWord("--advanced", 0) + "/" +  "\n\t\t\t\t\t" + colorWord("--all", 0) )
    # [h] Usage : python Aleph.py <keyword> --simple/--normal/--advanced/-all

def appendWordlist(new_list, list):
	for item in list:
		new_list.append(item)

def createWordlist(manipulator, mode):
	# Creates the wordlist
	if (mode == "simple"):
		manipulator.simpleManipulation(do_write = True)
	elif (mode == "normal"):
		manipulator.normalManipulation(do_write = True)
	elif (mode == "advanced"):
		manipulator.advancedManipulation(do_write = True)
	elif (mode == "all"):
		StandardFunc.dynamicPrint(signs.INFO + " Creating simple passwords.")
		list_simple = manipulator.simpleManipulation(do_write = False)
		StandardFunc.dynamicPrint(signs.INFO + " Creating normal passwords.")
		list_normal = manipulator.normalManipulation(do_write = False)
		StandardFunc.dynamicPrint(signs.INFO + " Creating advanced passwords.")
		list_advanced = manipulator.advancedManipulation(do_write = False)
		StandardFunc.dynamicPrint(signs.INFO + " Merging passwords")
		if ((list_simple != None) and (list_normal != None) and (list_advanced != None)):
			# Created all wordlists succesfully
			# the lists will now be merged and then written to disk.
			wordlists = []
			appendWordlist(wordlists, list_simple)
			appendWordlist(wordlists, list_normal)
			appendWordlist(wordlists, list_advanced)
			manipulator.writeAll(wordlists)
		else:
			print("Serious error, this is not supposed to happen at all!")
			exit(0)

if (len(sys.argv) < 3): # 2 Arguments required, word/url and mode (script name treated as argument 0)
	printHelp()
	exit(0)

keyword = sys.argv[1]
keywrds = keyword.split(',')
if (len(keywrds) > 1): # This tool isn't meant for multiple keywords.
	print("[+] Please use a different tool..")
	exit(0)

wordlist = []
keyword = keyword.replace(" ", "")
configuration = StandardFunc.readConfigFile()

if keyword.startswith("www."):
	# user inputs a URL without http://
	# lets be nice and add it for them.
	is_url = True
	print(signs.INFO + " " + keyword + " -> " + colorWord("http://" + keyword, 0 ))
	keyword = "http://" + keyword
else:
	is_url = re.search(r'https?://', keyword) # Checking if user input is a URL
if (is_url is not None):
	# If it indeed is a URL the WebListGenerator will spider for keywords which
	# are then manipulated by the WordlistManipulator.
	max_results = int(configuration['max_spider_results'])
	max_word_length = int(configuration['max_generator_word_length'])
	min_word_length = int(configuration['min_generator_word_length'])
	strict_ssl = StandardFunc.readBool(configuration['strict_ssl'])
	if (sys.argv[2] == '--simple'):
		web_generator = WebListGenerator(keyword, min_word_length, max_word_length, strict_ssl)
		datamuse_generator = DatamuseGenerator(web_generator.GetList(max_results))
		datamuse_list = datamuse_generator.find_similar_words("simple")
		manipulator = WordlistManipulator(datamuse_list, True)
		createWordlist(manipulator, "simple")
	elif (sys.argv[2] == '--normal'):
		web_generator = WebListGenerator(keyword, min_word_length, max_word_length, strict_ssl)
		datamuse_generator = DatamuseGenerator(web_generator.GetList(max_results))
		datamuse_list = datamuse_generator.find_similar_words("normal")
		manipulator = WordlistManipulator(datamuse_list, True)
		createWordlist(manipulator, "normal")
	elif (sys.argv[2] == '--advanced'):
		web_generator = WebListGenerator(keyword, min_word_length, max_word_length, strict_ssl)
		datamuse_generator = DatamuseGenerator(web_generator.GetList(max_results))
		datamuse_list = datamuse_generator.find_similar_words("advanced")
		manipulator = WordlistManipulator(datamuse_list, True)
		createWordlist(manipulator, "advanced")
	elif (sys.argv[2] == '--all'):
		web_generator = WebListGenerator(keyword, min_word_length, max_word_length, strict_ssl)
		datamuse_generator = DatamuseGenerator(web_generator.GetList(max_results))
		datamuse_list = datamuse_generator.find_similar_words("advanced")
		manipulator = WordlistManipulator(datamuse_list, True)
		createWordlist(manipulator, "all")
	else:
		printHelp()
elif (is_url is None):
	# If it's just a regular keyword

	wordlist.append(keyword)
	manipulator = WordlistManipulator(wordlist, False)

	if (sys.argv[2] == '--simple'):
		createWordlist(manipulator, "simple")
	elif (sys.argv[2] == '--normal'):
		createWordlist(manipulator, "normal")
	elif (sys.argv[2] == '--advanced'):
		createWordlist(manipulator, "advanced")
	elif (sys.argv[2] == '--all'):
		createWordlist(manipulator, "all")
	else:
		printHelp()
