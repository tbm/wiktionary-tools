"""
Functions to work with Wiktionary entries
"""

import re

from .lang import lang_map


def get_entry(text, lang):
    """
    Get the entry for a specific language from a text
    """
    if lang not in lang_map:
        raise NotImplementedError(f"Unsupported language: {lang}")
    start = text.find(f"=={lang_map[lang]}==")
    if start == -1:
        return None
    text = text[start:]
    end = re.search(r"\n==[^=]", text)
    if end:
        return text[: end.start()]
    return text
