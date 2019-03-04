
from bs4 import BeautifulSoup
from collections import Counter
import urllib.request
import re
from standard_functions import *
from wordlist_manipulation import *
class WebListGenerator():

    def __init__(self, url, completeness, minwordlength, maxwordlength):
        #Simple webspider that creates a list of all unique words in a given webpage.
        self.url = url
        self.completeness = completeness
        self.minwordlength = minwordlength
        self.maxwordlength = maxwordlength
        html = urllib.request.urlopen(self.url).read()
        soup = BeautifulSoup(html, features='lxml')
        self.URLlist = [self.url]
        subUrlList = self.FindSubUrls(soup)
        for url in subUrlList:
            self.URLlist.append(url)
        rawList = self.SearchWebpage(self.URLlist)
        uniqueList = self.CommonWebList(rawList, self.completeness)
        self.cleanList = self.CleanWebList(uniqueList, self.minwordlength, self.maxwordlength)

    def FindSubUrls(self, soup):
        #search given url for other links and adds them to sub-urlList
        StandardFunc.dynamicPrint(signs.PLUS + " Searching webpage for links.")
        links = soup.find_all('a')
        subUrls = []
        for tag in links:
            link = tag.get('href', None)
            if link is not None:
                match = re.search(r'https?', link)
                if match is not None:
                    subUrls.append(link)
        return subUrls

    def SearchWebpage(self, URLlist):
        #looks at urls in urllist and adds all found words to list
        wordlist = []
        StandardFunc.dynamicPrint(signs.PLUS + "Found all links. Getting words from all webpages...")
        for url in URLlist:
            try:
                html = urllib.request.urlopen(url).read()
                soup = BeautifulSoup(html, features='lxml')
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                allWords = list(re.sub(r"([A-Z])", r"\n\1", text).split())
                for word in allWords:
                    wordlist.append(word)
            except:
                continue
        StandardFunc.dynamicPrint(signs.PLUS + " Found all words.")
        self.NormalizeWords(wordlist)
        return wordlist

    def CommonWebList(self, wordlist, completeness):
        #returns common values from SearchWebAll, whereas completeness is a number between 1 - 100 that determines how much of the found words are returned
        totallength = len(set(wordlist))
        returnnbr = totallength * completeness / 100
        counter = Counter(wordlist)
        counttuple = counter.most_common(int(returnnbr))
        wordlist = [x[0] for x in counttuple]
        return wordlist

    def CleanWebList(self, wordlist, minwordlength, maxwordlength):
        #takes a weblist and checks it on length
        copylist = wordlist.copy() #needed for weird bug, otherwise list is not being iterated totally
        for word in copylist:
            if (word == '') or (len(word) < minwordlength) or (len(word) > maxwordlength):
                wordlist.remove(word)
        StandardFunc.dynamicPrint(signs.PLUS + "Cleaned results.")
        return wordlist

    def NormalizeWords(self, wordlist):
        #Gets rid of all capital letters and weird characters.
        for x in range(len(wordlist)):
            wordlist[x] = wordlist[x].lower()
            wordlist[x] = re.sub(r'[^a-z]+', '', wordlist[x])

    def GetList(self):
        return self.cleanList
