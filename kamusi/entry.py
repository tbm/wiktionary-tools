# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Functions to work with Wiktionary entries
"""

__license__ = "GPL-3.0-or-later"

import re

import kamusi


def get_entry(text, lang, site="en", strip=False):
    """
    Get the entry for a specific language from a text
    """
    lang_name = kamusi.code_to_name(lang, site)
    if site == "sv":
        lang_name = lang_name.title()
    start = text.find("==" + lang_name + "==")
    if start == -1:
        return None
    text = text[start:]
    end = re.search(r"\n==[^=]", text)
    if end:
        text = text[: end.start() + 1]
    if strip:
        return text.rstrip()
    return text


def get_section(entry, title):
    """
    Return a specific section of an entry
    """
    loc = entry.find("===" + title + "===")
    if loc == -1:
        return None
    entry = entry[loc:]
    loc = entry.find("\n\n")
    if loc == -1:
        return entry
    return entry[: loc + 1]
