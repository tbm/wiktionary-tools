"""
Functions for Yiddish for Swedish Wiktionary
"""

import re

import mwparserfromhell

import isofyi


def get_section(entry, title):
    """
    Return a specific section of an entry from Swedish Wiktionary
    """
    loc = entry.find("===" + title + "===")
    if loc == -1:
        return None
    entry = entry[loc:]
    loc = entry.find("\n\n")
    if loc == -1:
        return entry
    return entry[: loc + 1]


def get_noun_section(entry):
    """
    Return the Noun section of an entry from Swedish Wiktionary
    """
    return get_section(entry, "Substantiv")


def get_verb_section(entry):
    """
    Return the Verb section of an entry from Swedish Wiktionary
    """
    return get_section(entry, "Verb")


def get_parts(entry):
    """
    Get the individual parts (definitions) of an entry or section
    """
    loc = entry.find("\n")
    for part in re.findall(r"((?:\{\{.*\}\}\n)+'''.*\n)", entry):
        yield part


def gender_sort(item):
    """
    Sort gender identifies in the same way as English Wiktionary
    """
    order = {"m": 0, "f": 1, "n": 2}
    return order.get(item, float("inf"))


def get_gender(templates):
    """
    Get the gender from templates
    """
    genders = set()
    template_names = [str(template.name) for template in templates]
    for name in template_names:
        if name in ("subst", "länk"):
            continue
        if name.startswith("yi-subst-"):
            name = name.split("-")[2]
        if name.endswith("pl"):
            name = name[:2]
        # We can have {{mf}} plus {{yi-subst-m-s}} and {{yi-subst-f-s}},
        # leading to mf + m + f
        if name == "mf":
            genders.update([char for char in name])
        else:
            genders.add(name)
    if not genders:
        return None
    return "".join(sorted(genders, key=gender_sort))


def get_noun(entry_name, entry):
    """
    Get a noun from an entry from Swedish Wiktionary
    """
    # We have to cut the entry because later information (e.g. etymology)
    # can contain unrelated gender
    section = entry[: entry.find("\n#")]
    wikicode = mwparserfromhell.parse(section)
    templates = wikicode.filter_templates()
    gender = get_gender(templates)
    return isofyi.YiddishNoun(entry_name, gender, None)


def get_verb(entry_name, entry):
    """
    Get a Verb from an entry from Swedish Wiktionary
    """
    if "{{verb|yi}}" in entry:
        return isofyi.YiddishVerb(entry_name, None)
    return None


def parse_entry(entry_name, entry):
    """
    Return a YiddishFoo() named tuple for an entry from Swedish Wiktionary
    """
    if "===Substantiv===" in entry:
        for part in get_parts(get_noun_section(entry)):
            yield get_noun(entry_name, part)
    if "===Verb===" in entry:
        for part in get_parts(get_verb_section(entry)):
            yield get_verb(entry_name, part)
