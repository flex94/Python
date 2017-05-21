# -*- coding: utf-8 -*-
"""Helper functions for cpabien"""

# import pdb
import shutil
import requests
import unicodedata
from HTMLParser import HTMLParser
from ..utils.yesno import query_oui_non
import sys


class SearchResultParser(HTMLParser):
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

class DlPageParser(HTMLParser):
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
    parser = SearchResultParser()
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
    parser = DlPageParser()
    parser.feed(resp.text)
    return 'http://www.cpabien.xyz' + parser.dl_url

def downloadTorrentForInput(inputString):
    targetUrl = 'http://cpabien.xyz/search.php'

    searchString = cleanInputString(inputString)
    searchRequest = requests.post(targetUrl, data={'t': searchString})
    results = processAndFilterSearchResult(searchRequest)

    return results

while True:
    sys.stdout.write("\nSaisir le nom d'un film et appuyer sur Enter.\n " +
    "(Appuyer directement sur Enter pour quitter)\n")
    inputString = raw_input().lower()

    if not(inputString):
        break

    results = downloadTorrentForInput(inputString)
    nbResults = len(results)
    hintStr = '\nVerifier que le titre est correctement orthographie. ' + \
                'Sinon, le film n\'est peut etre pas disponible.'
    if not(nbResults):
        print 'Pas de resultat pour "%s". ' % inputString + hintStr
    else:
        print '%g resultats trouves\n' % nbResults
        for resu in results:
            dlTitle = resu['title']
            ans = query_oui_non('%s - Est-ce le bon film?' % dlTitle)

            if ans:
                dlUrl = getDlUrl(resu['rawUrl'])

                req = requests.get(dlUrl, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
                if req.status_code == 200:
                    with open("%s.torrent" % cleanInputString(inputString), 'wb') as f:
                        req.raw.decode_content = True
                        shutil.copyfileobj(req.raw, f)

                print 'Telechargement de "%s" lance!' % dlTitle
                break
        else:
            print '\nFin des resultats pour "%s"! ' % inputString + hintStr
