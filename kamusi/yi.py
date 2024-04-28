"""
Functions for Yiddish
"""

import re

import mwparserfromhell

import isofyi


def get_val(template, name):
    """
    Return value of template paramater or None
    """
    if template.has(name):
        return template.get(name).value
    return None


def parse_entry(entry_name, entry):
    """
    Return a YiddishFoo() named tuple
    """
    for line in entry.splitlines(keepends=True):
        # This is just a speed optimization over calling mwparserfromhell
        # on the whole entry
        if not re.search(r"\{\{(yi-noun|yi-verb)", line):
            continue
        wikicode = mwparserfromhell.parse(line)
        for template in wikicode.filter_templates():
            if str(template.name) in ("yi-noun", "yi-proper noun"):
                yield isofyi.YiddishNoun(
                    entry_name, get_val(template, "g"), get_val(template, "pl")
                )
            elif template.name == "yi-verb":
                yield isofyi.YiddishVerb(entry_name, get_val(template, "1"))
