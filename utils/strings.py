# -*- coding: utf-8 -*-
"""String functions."""

import unicodedata

def clean_str(s):
    """Remove accents and encode in utf-8."""
    s = unicode(s, 'utf-8')
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore')
    return s
