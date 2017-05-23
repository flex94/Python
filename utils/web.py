"""Web utils."""
# import pdb
import lxml.html as lh
import urllib
import urllib2

def open_url(url, data={}, user_agent='Mozilla/5.0'):
    """Get a webpage content from its url.

    Returns a response ready to be parsed with lxml.
    data: POST data (optional)
    user_agent: defaults to Mozilla (optional)
    """
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', user_agent)]

    if len(data):
        response = opener.open(url, urllib.urlencode(data))
    else:
        response = opener.open(url)

    return response

def parse_with_filter(resp, elt, attr, val):
    """Return all elements from the page that match attr's value == val.

    resp: urllib2 opener - use result from open_url
    elt: string - e.g. div, a
    attr: string - e.g. class, id
    val: string
    """
    doc = lh.parse(resp)

    return filter(lambda e: e.get(attr) == val, doc.iter(elt))


# Examples
# url = 'http://cpabien.xyz/search.php'
# data = {'t': 'muraille'}
# resp = open_url(url, data)
# resu = parse_with_filter(resp, 'a', 'class', 'titre')
# pdb.set_trace()
