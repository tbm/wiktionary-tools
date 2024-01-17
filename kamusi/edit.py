"""
Edit Wiktionary pages
"""

import re


def add_category(entry, category, lang):
    """
    Add category to entry
    """

    if re.search(r"({{(C|c|topics)\||\[\[Category:)", entry):
        print("Page already has category")
        return entry

    cat = "\n{{C|" + lang + "|" + category + "}}\n"
    if entry[-1] != "\n":
        entry += "\n" + cat
    else:
        entry += cat
    return entry


def add_thumbnail(entry, thumbnail, description=None):
    """
    Add thumbnail to entry
    """
    if "[[File:" in entry or "[[Image:" in entry:
        return entry
    if not thumbnail.startswith("File:"):
        thumbnail = "File:" + thumbnail
    if description:
        description = "|" + description
    else:
        description = ""
    link = "[[" + thumbnail + "|thumb" + description + "]]"
    first_break = entry.find("\n") + 1
    return entry[:first_break] + link + "\n" + entry[first_break:]


def add_wikipedia(entry, lang, wikipedia=None):
    """
    Add Wikipedia link to entry
    """
    if "{{wikipedia" in entry or "{{wp" in entry:
        return entry
    first_break = entry.find("\n\n") + 1
    wp = "{{wikipedia"
    if wikipedia:
        wp += "|" + wikipedia
    if lang != "en":
        wp += "|lang=" + lang
    wp += "}}"
    return entry[:first_break] + wp + "\n" + entry[first_break:]
