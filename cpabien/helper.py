# -*- coding: utf-8 -*-
"""Helper functions for cpabien."""

from ..utils.strings import clean_str
from ..utils.web import open_url, parse_with_filter

def __get_result_rows(resp):
    def filtr(val):
        return (type(val) is str and 'ligne' in val)

    return parse_with_filter(resp, 'div', 'class', filtr)

def __postprocess_results(raw_data):
    results = []

    for row in raw_data:
        resu = {}
        resu['item_url'] = row[0].get('href')
        resu['title'] = row[0].text
        resu['size'] = __process_size(row[1].text)
        resu['seed'] = int(row[2][0].text)
        results.append(resu)

    return results

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

def search_torrents(input_str):
    """Search torrents, filter and enrich results.

    Returns a list of objects ready to be displayed.
    """
    search_url = 'http://cpabien.xyz/search.php'

    resp = open_url(search_url, {'t': clean_str(input_str)})
    rows = __get_result_rows(resp)
    results = __postprocess_results(rows)

    return results

def get_dl_url(item_url):
    """Parse the item page url to return the file url."""
    resp = open_url(item_url)
    suffix = parse_with_filter(resp, 'a', 'id', 'telecharger')[0].get('href')
    return 'http://www.cpabien.xyz' + suffix
