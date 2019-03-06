
from bs4 import BeautifulSoup, Comment
from collections import Counter
import urllib.request
import ssl
import re
from standard_functions import *
from wordlist_manipulation import *

class WebListGenerator():

    def __init__(self, url, minwordlength, maxwordlength, strictssl):
        #Simple webspider that creates a list of all unique words in a given webpage.
        self.url = url
        if self.url.endswith('/'):
            self.url = self.url[:-1]
        self.minwordlength = minwordlength
        self.maxwordlength = maxwordlength
        self.strictssl = strictssl
        if strictssl:
            html = urllib.request.urlopen(self.url).read()
        else:
            ctx = ssl.SSLContext()
            ctx.verify_mode = ssl.CERT_NONE
            html = urllib.request.urlopen(self.url, context=ctx).read()
        soup = BeautifulSoup(html, features='lxml')
        self.URLlist = [self.url]
        subUrlList = self.FindSubUrls(soup)
        for url in subUrlList:
            self.URLlist.append(url)
        weblist = self.create_weblist(self.URLlist)
        normalized_list = self.normalize_words(weblist)
        common_list = self.CommonWebList(normalized_list)
        uniqueList = self.findUniqueWords(self.url)
        for word in uniqueList:
            common_list.append(word)
        self.cleanList = self.CleanWebList(common_list, self.minwordlength, self.maxwordlength)

    def FindSubUrls(self, soup):
        #search given url for other links and adds them to sub-urlList
        configuration = StandardFunc.readConfigFile()
        only_subdomains = configuration['only_spider_subdomains']
        StandardFunc.dynamicPrint(signs.PLUS + " Searching webpage for links.")
        links = soup.find_all('a')
        subUrls = []
        for tag in links:
            link = tag.get('href', None)
            if link is not None:
                if only_subdomains == 'True':
                    if (str(link).startswith(self.url)):
                        subUrls.append(link)
                    elif (str(link).startswith('/')):
                        subUrls.append(self.url + link)
                if only_subdomains == 'False':
                    match = re.search(r'https?', link)
                    if match is not None:
                        subUrls.append(link)
        return subUrls

    def isVisible(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'meta']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def read_web_page(self, url):
        #returns a list of all words on a given webpage
        if self.strictssl:
            html = urllib.request.urlopen(url).read()
        else:
            ctx = ssl.SSLContext()
            ctx.verify_mode = ssl.CERT_NONE
            html = urllib.request.urlopen(self.url, context=ctx).read()
        soup = BeautifulSoup(html, 'lxml')
        text = soup.findAll(text=True)
        text = filter(self.isVisible, text)
        text = u" ".join(t.strip() for t in text)
        #lines = (line.strip() for line in text.splitlines())
        #chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        #text = '\n'.join(chunk for chunk in chunks if chunk)
        wordlist = list(re.sub(r"([A-Z])", r"\n\1", text).split())
        return wordlist

    def create_weblist(self, URLlist):
        #looks at urls in urllist and adds all found words to list
        wordlist = []

        StandardFunc.dynamicPrint(signs.PLUS + " Found all links. Getting words from webpages. (This may take a while...)\n")
        for url in URLlist:
            try:
                allWords = self.read_web_page(url)
                StandardFunc.dynamicPrint(signs.INFO + " Crawling "+ colorWord(url,0))
                for word in allWords:
                    wordlist.append(word)
            except Exception as e:
                #print(e)
                continue
        StandardFunc.dynamicPrint(signs.PLUS + " Found all words. ")
        return wordlist


    def findUniqueWords(self, url):
        #returns a list of all unique (only appear one time) words in given webpage
        wordlist = self.read_web_page(url)
        totallength = len(set(wordlist))
        counter = Counter(wordlist)
        counttuple = counter.most_common(totallength)
        setlist = []
        for x in counttuple:
            if x[1] == 1:
                setlist.append(x[0])
        return setlist

    def CommonWebList(self, wordlist):
        #returns hierarchical common values from SearchWebAll\
        totallength = len(set(wordlist))
        counter = Counter(wordlist)
        counttuple = counter.most_common(totallength)
        sublist = []
        for word in counttuple:
            sublist.append(word[0])
        return sublist

    def CleanWebList(self, wordlist, minwordlength, maxwordlength):
        #returns a list of words that match specified length
        copylist = wordlist.copy()
        for word in copylist:
            if (word == '') or (len(word) < minwordlength) or (len(word) > maxwordlength):
                wordlist.remove(word)
        StandardFunc.dynamicPrint(signs.PLUS + " Cleaned results. \n")
        return wordlist

    def normalize_words(self, wordlist):
        #Gets rid of all capital letters and weird characters.
        for x in range(len(wordlist)):
            wordlist[x] = wordlist[x].lower()
            wordlist[x] = re.sub(r'[^a-z]+', '', wordlist[x])
        return wordlist

    def GetList(self, weblist_length):
        if len(self.cleanList) > weblist_length:
            return self.cleanList[0:weblist_length]
        else:
            return self.cleanList
