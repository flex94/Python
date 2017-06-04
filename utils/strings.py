# -*- coding: utf-8 -*-
"""String functions."""

import unicodedata

def clean_str(s):
    """Remove all accents from an input string or unicode.

	Use after receiving an input from user or before printing to console.
	s: utf-8 encoded string or unicode, with accents
	return: ascii encoded string without accents
	"""
    if not isinstance(s, unicode):
	    s = unicode(s, 'utf-8')

    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore')
    return s
