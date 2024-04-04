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

    cat = "{{C|" + lang + "|" + category + "}}\n"
    return entry.rstrip() + "\n\n" + cat + "\n"


def add_ety_ref(entry, ref):
    """
    Add a reference to the etymology
    """
    loc = entry.find("}}.") + 3
    entry = entry[:loc] + ref + entry[loc:]
    return add_reflist(entry)


def add_ref(entry, ref):
    """
    Add a reference to the "References" section
    """
    loc = entry.find("===References===")
    if loc != -1:
        loc = entry.find("\n\n", loc) + 1
        return entry[:loc] + ref + "\n" + entry[loc:]

    loc = entry.find("===Further reading===")
    if loc == -1:
        loc = entry.find("===Anagrams===")
    if loc == -1:
        if match := re.search(r"(\{\{\s*(topics|c|C)\s*\||\[\[Category:\w+:)", entry):
            loc = match.start()
    ref = "===References===\n" + ref + "\n\n"
    return entry[:loc] + ref + entry[loc:]


def add_reflist(entry):
    """
    Add "{{reflist}"" to the "References" section
    """
    if "{{reflist}}" in entry:
        return entry
    if re.search(r"<references\s*/>", entry):
        return entry
    return add_ref(entry, "{{reflist}}")


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
