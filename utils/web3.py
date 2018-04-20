"""Web utils python3."""
import httplib2
from urllib.parse import urlencode
import lxml.html as lh
import pdb

USER_AGENT_MOZILLA = 'Mozilla/5.0'

def request(url, data={}, user_agent=USER_AGENT_MOZILLA):
    """Get a webpage content from its url.

    Returns a response ready to be parsed with lxml.

    data: POST data (optional)
    user_agent: defaults to Mozilla (optional)
    """
    h = httplib2.Http('.cache')
    args = (url,)
    if len(data):
        args += ('POST', urlencode(data))
    resp, content = h.request(*args, headers={'User-Agent': USER_AGENT_MOZILLA})
    return content

resp = request("https://www.google.com")
doc = lh.parse # does not work...
pdb.set_trace()
print('fin')
