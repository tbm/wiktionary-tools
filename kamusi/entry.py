"""
Functions to work with Wiktionary entries
"""

import re

import kamusi


def get_entry(text, lang, strip=False):
    """
    Get the entry for a specific language from a text
    """
    start = text.find("==" + kamusi.code_to_name(lang) + "==")
    if start == -1:
        return None
    text = text[start:]
    end = re.search(r"\n==[^=]", text)
    if end:
        text = text[: end.start()+1]
    if strip:
        return text.rstrip()
    return text
