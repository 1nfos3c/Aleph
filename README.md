# Aleph

Hi! This is **Aleph**, a one word wordlist generator.

![Aleph](http://i67.tinypic.com/9kwgfs.png)

### Compatibility
**Aleph** works with **Python3** on both **Linux** and **OSX**.
To install the required dependencies use:  
```pip3 install -r requirements.txt```

### Usage
Just give **Aleph** a single keyword or URL and a mode and it will create a wordlist based on that.   
Specific configuration options can be edited in the config file located in ```src/```.

### Modes  
There are four modes to choose from:  
```--simple``` , ```--normal```, ```--advanced``` and ```--all``` .  
The first three modes each create unique passwords and 
```-all``` simply generates all of them.  

### Spider
When supplied with a URL, **Aleph** will scrape the webpage and its links for unique words.  
These words will then be used to search for similar words using Datamuse.  
This list of keywords will then be used to create the wordlist.
A website about coffee would for example create a wordlist with words like coffee, beans, cappucino etc.  
