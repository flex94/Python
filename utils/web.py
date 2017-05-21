"""Web utils."""
import lxml.html as lh
import urllib2
# import pdb

def __open_url_w_user_agent(url, user_agent='Mozilla/5.0'):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', user_agent)]
    response = opener.open(url)
    return response

def doc_from_url(url):
    """Open url and prepare for parsing with lxml."""
    resp = __open_url_w_user_agent(url)
    return lh.parse(resp)

def parse_with_filter(doc, elt, attr, val):
    """Return all elements from doc that match attr's value == val."""
    return filter(lambda e: e.get(attr) == val, doc.iter(elt))

# Examples
# url = 'http://9docu.com'
# doc = doc_from_url(url)
# resu = parse_with_filter(doc, 'div', 'class', 'data')
