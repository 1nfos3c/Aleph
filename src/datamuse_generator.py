from datamuse import datamuse
from standard_functions import *
from wordlist_manipulation import *

class DatamuseGenerator:

    def __init__(self, wordlist):
        self.api = datamuse.Datamuse()
        self.wordlist = wordlist

    def find_similar_words(self, mode):
        similar_list = self.wordlist.copy()
        configuration = StandardFunc.readConfigFile()
        only_subdomains = configuration['only_spider_subdomains']
        if mode == "simple":
            return_nr = int(configuration['simple_datamuse_max_results'])
        if mode == "normal":
            return_nr = int(configuration['normal_datamuse_max_results'])
        if mode == "advanced":
            return_nr = int(configuration['advanced_datamuse_max_results'])
        for word in self.wordlist:
            StandardFunc.dynamicPrint(signs.INFO + " Found words on webpages. Creating similar words for: " + colorWord(str(word),0))
            similar_dict = self.api.words(rel_trg=word, max=return_nr)
            species_dict = self.api.words(rel_spc=word, max=return_nr)
            for word in similar_dict:
                similar_list.append(word['word'])
            for word in species_dict:
                similar_list.append(word['word'])
        similar_list = list(set(similar_list))
        print(" ")
        return similar_list
