"""Web utils."""
import lxml.html as lh
import urllib
import urllib2
import requests
from shutil import copyfileobj

USER_AGENT_MOZILLA = 'Mozilla/5.0'

def open_url(url, data={}, user_agent=USER_AGENT_MOZILLA):
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

def parse_with_filter(resp, elt, attr, f):
    """Return all elements from the page that match attr's value == val.

    resp: urllib2 opener - use result from open_url
    elt: string - e.g. div, a
    attr: string - e.g. class, id
    f: string or lambda
    """
    doc = lh.parse(resp)

    if callable(f):
        def filtr(e):
            return f(e.get(attr))
    else:
        def filtr(e):
            return e.get(attr) == f

    return filter(filtr, doc.iter(elt))

def dl_file(url, name, user_agent=USER_AGENT_MOZILLA):
    """Download file from url and write to current folder."""
    req = requests.get(url, stream=True, headers={'User-Agent': user_agent})
    if req.status_code == 200:
        with open(name, 'wb') as f:
            req.raw.decode_content = True
            copyfileobj(req.raw, f)
        return True
    return False


""" Examples

url = 'http://cpabien.xyz/search.php'
data = {'t': 'muraille'}
resp = open_url(url, data)

def filtr(val):
    return (type(val) is str and 'ligne' in val)
resu = parse_with_filter(resp, 'div', 'class', filtr)

Then can do resu[0][0].get('href')...

"""

