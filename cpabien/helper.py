# -*- coding: utf-8 -*-
"""Helper functions for cpabien."""

# import pdb
import requests
import unicodedata
from HTMLParser import HTMLParser
from shutil import copyfileobj
from ..utils.strings import clean_str

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

def __process_size(s):
    """Take a string with unit, return a float in Mo."""
    [size, unit] = s.split(' ')
    size = float(size)
    if unit == 'Go':
        size *= 1000
    return size

def __filter_data(row):
    """Filter a search result based on size and seed."""
    size, seed = row['size'], row['seed']
    return size > 500 and size < 2000 and seed > 0

def __postprocess_results(resp):
    parser = __SearchResultParser()
    parser.feed(resp.text)
    raw_data = parser.rows

    data = map(
        lambda x: {k: e for k, e in
            zip(['raw_url', 'title', 'size', 'seed', 'leech'],
            map(lambda s: unicodedata.normalize('NFD', s).encode('ascii', 'ignore'), x))},
        raw_data
    )

    for r in data:
        r['size'] = __process_size(r['size'])
        r['seed'] = int(r['seed'])
        r['dl_url'] = __dl_url(r['raw_url'])

    data = filter(__filter_data, data)
    return data

def __dl_url(url):
    resp = requests.get(url)
    parser = __DlPageParser()
    parser.feed(resp.text)
    return 'http://www.cpabien.xyz' + parser.dl_url

def search_torrents(input_str):
    """Search torrents, filter and enrich results."""
    target_url = 'http://cpabien.xyz/search.php'

    search_str = clean_str(input_str)
    search_req = requests.post(target_url, data={'t': search_str})
    results = __postprocess_results(search_req)

    return results

def dl_file(url, name):
    """Download torrent file from url."""
    req = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
    if req.status_code == 200:
        with open("%s.torrent" % name, 'wb') as f:
            req.raw.decode_content = True
            copyfileobj(req.raw, f)
        return True
    return False
