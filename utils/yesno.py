# -*- coding: utf-8 -*-

"""Yes/No input utils."""
import sys

def query_oui_non(question, default="oui"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {
        "oui": True, "o": True, "O": True, 
        "non": False, "n": False, "N": False
    }
    if default is None:
        prompt = " [o/n] "
    elif default == "oui":
        prompt = " [O/n] "
    elif default == "non":
        prompt = " [o/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Répondre par o (oui) ou n (non).\n")
