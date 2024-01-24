"""
Show colour diff

Taken from StackOverflow:
https://stackoverflow.com/questions/32500167/how-to-show-diff-of-two-string-sequences-in-colors

License unknown
"""

import difflib


def red(text):
    """Format text in red"""
    return f"\033[38;2;255;0;0m{text}\033[38;2;255;255;255m"


def green(text):
    """Format text in green"""
    return f"\033[38;2;0;255;0m{text}\033[38;2;255;255;255m"


def blue(text):
    """Format text in blue"""
    return f"\033[38;2;0;0;255m{text}\033[38;2;255;255;255m"


def white(text):
    """Format text in white"""
    return f"\033[38;2;255;255;255m{text}\033[38;2;255;255;255m"


def colour_diff(old, new):
    """
    Return colour diff
    """
    result = ""
    codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
    for code in codes:
        if code[0] == "equal":
            result += white(old[code[1] : code[2]])
        elif code[0] == "delete":
            result += red(old[code[1] : code[2]])
        elif code[0] == "insert":
            result += green(new[code[3] : code[4]])
        elif code[0] == "replace":
            result += red(old[code[1] : code[2]]) + green(new[code[3] : code[4]])
    return result
