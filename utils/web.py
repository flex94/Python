"""Web utils."""
import lxml.html as lh
import urllib2
# import pdb

def doc_from_url(url):
    """Open url and prepare for parsing with lxml."""
    return lh.parse(urllib2.urlopen(url))

def parse_with_filter(doc, elt, attr, val):
    """Return all elements from doc that match attr's value == val."""
    return filter(lambda e: e.get(attr) == val, doc.iter(elt))

# Examples
# url = 'http://9docu.com'
# doc = doc_from_url(url)
# resu = parse_with_filter(doc, 'div', 'class', 'data')
