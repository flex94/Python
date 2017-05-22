# -*- coding: utf-8 -*-
"""Helper functions for cpabien."""

# import pdb
import requests
import unicodedata
from HTMLParser import HTMLParser

class __SearchResultParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.rows = []
        self.currentRow = []
        self.debug = 0

    def handle_starttag(self, tag, attributes):
        if self.recording and tag != 'br' and tag != 'img':
            self.recording += 1
            if self.debug:
                print 'start tag:%s - Changing recording to %g' % (tag, self.recording)
            if tag == 'a':
                for (name, value) in attributes:
                    if name == "href":
                        self.currentRow.append(value)
            return
        if tag != 'div':
            return
        for name, value in attributes:
            if name == 'class' and value.find('ligne') >= 0:
                if self.debug:
                    print 'start tag: %s - Starting recording' % tag
                    print attributes
                self.recording = 1
                self.currentRow = []
                return
        return

    def handle_endtag(self, tag):
        if self.recording and tag != 'br' and tag != 'img':
            self.recording -= 1
            if self.recording == 0:
                self.rows.append(self.currentRow)
            if self.debug:
                print 'end tag:%s - Changing recording to %g' % (tag, self.recording)

    def handle_data(self, data):
        if self.recording:
            self.currentRow.append(data)

class __DlPageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.dl_url = ''
        self.debug = 0

    def handle_starttag(self, tag, attributes):
        if self.recording and tag != 'br' and tag != 'img':
            self.recording += 1
            if self.debug:
                print 'start tag:%s - Changing recording to %g' % (tag, self.recording)
            if tag == 'a':
                for (name, value) in attributes:
                    if name == "href":
                        self.dl_url = value
            return
        if tag != 'div':
            return
        for name, value in attributes:
            if name == 'id' and value.find('infosficher') >= 0:
                if self.debug:
                    print 'start tag: %s - Starting recording' % tag
                    print attributes
                self.recording = 1
                return
        return

    def handle_endtag(self, tag):
        if self.recording and tag != 'br' and tag != 'img':
            self.recording -= 1
            if self.debug:
                print 'end tag:%s - Changing recording to %g' % (tag, self.recording)


def cleanInputString(s):
    s = unicode(s, 'utf-8')
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore')
    return s

def processSize(s):
    [size, unit] = s.split(' ')
    size = float(size)
    if unit == 'Go':
        size *= 1000
    return size

def filterData(row):
    size, seed = row['size'], row['seed']
    return size > 500 and size < 2000 and seed > 0

def processAndFilterSearchResult(resp):
    parser = __SearchResultParser()
    parser.feed(resp.text)
    rawData = parser.rows

    data = map(
        lambda x: {k: e for k, e in
            zip(['rawUrl', 'title', 'size', 'seed', 'leech'],
            map(lambda s: unicodedata.normalize('NFD', s).encode('ascii', 'ignore'), x))},
        rawData
    )

    for r in data:
        r['size'] = processSize(r['size'])
        r['seed'] = int(r['seed'])

    data = filter(filterData, data)
    return data

def getDlUrl(url):
    resp = requests.get(url)
    parser = __DlPageParser()
    parser.feed(resp.text)
    return 'http://www.cpabien.xyz' + parser.dl_url

def downloadTorrentForInput(inputString):
    targetUrl = 'http://cpabien.xyz/search.php'

    searchString = cleanInputString(inputString)
    searchRequest = requests.post(targetUrl, data={'t': searchString})
    results = processAndFilterSearchResult(searchRequest)

    return results
