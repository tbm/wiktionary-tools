#!/usr/bin/env python3

# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

__license__ = "GPL-3.0-or-later"

"""
Module to parse information from the Svensk-jiddisch-svensk ordbok
(Swedish-Yiddish-Swedish dictionary), published by the Swedish Institute
or Language and Folklore (ISOF).

A JSON file of this dictionary can be obtained from:
https://sprakresurser.isof.se/jiddisch/job.json
The license is CC0 1.0.
"""

from collections import namedtuple
import json
import logging
import re

logger = logging.getLogger(__name__)

YiddishAdjective = namedtuple("YiddishAdjective", ["word"])
YiddishAdverb = namedtuple("YiddishAdverb", ["word"])
YiddishConjunction = namedtuple("YiddishConjunction", ["word"])
YiddishInterjection = namedtuple("YiddishInterjection", ["word"])
YiddishNoun = namedtuple("YiddishNoun", ["word", "gender", "plural"])
YiddishPreposition = namedtuple("YiddishPreposition", ["word"])
YiddishVerb = namedtuple("YiddishVerb", ["word", "past_participle"])

RE_NOUN = re.compile(r"(?P<word>[^,]+),\s+(?P<article>[^ ]+)\s*(\[(?P<plural>.+)\])?")


def get_graminfo(entry):
    """
    Get the graminfo (a classification of the grammar type)
    """
    return entry["sv"].get("graminfo")


def get_yiddish(entry):
    """
    Get the Yiddish information from the data structure
    """
    hebr = entry["yi"]["ord"]["Hebr"]
    hebr = hebr.replace("\u2067", "").replace("\u2069", "")
    return hebr


def get_data(json_file):
    """
    Get all the data from the JSON file
    """
    with open(json_file, "r", encoding="utf-8") as stream:
        for entry in json.load(stream):
            if not get_graminfo(entry):
                continue
            yield entry


def get_entry_by_id(data, number):
    """
    Get a specific entry from the JSON data by ID
    """
    for entry in data:
        if int(entry["ID"]) == number:
            return entry
    return None


def parse_adjective(info):
    """
    Parse adjectives
    """
    return YiddishAdjective(info)


def parse_adverb(info):
    """
    Parse adverbs
    """
    return YiddishAdverb(info)


def parse_conjunction(info):
    """
    Parse conjunctions
    """
    return YiddishConjunction(info)


def parse_interjection(info):
    """
    Parse interjections
    """
    return YiddishInterjection(info.rstrip("!"))


def get_gender(article):
    """
    Get gender from an article
    """
    article = article.replace("\\", "/")
    map_article_gender = {
        "דער": "m",  # der
        "די": "f",  # di
        "דאָס": "n",  # dos
        "דער/די": "mf",  # der/di
        "דער/דאָס": "mn",  # der/dos
        "דאָס/די": "fn",  # dos/di
        "די/דער": "mf",  # di/der
        "דאָס/דער": "mn",  # dos/der
        "די/דאָס": "fn",  # di/dos
    }
    if article not in map_article_gender:
        logger.error("Unknown article: %s", article)
    return map_article_gender.get(article)


def get_plural(plural):
    """
    Parse plural information
    """
    map_plural_endings = {
        "־ען": "en",
        "־ער": "er",
        "־עס": "es",
        # "־ות": "es", # es but can't use pl=es in Wiktionary?
        "־ן": "n",
        "־ס": "s",
        "־ים": "im",  # ?
        "־עך": "ech",  # ?
        "־": None,
    }
    if not plural:
        return plural
    if plural in map_plural_endings:
        return map_plural_endings[plural]
    if plural.startswith("־"):
        logger.error("Unknown plural ending: %s", plural)
        return plural
    return plural


def parse_noun(info):
    """
    Parse nouns
    """
    match = re.match(RE_NOUN, info)
    if not match:
        logger.error("Can't parase noun: %s", info)
        return None
    gender = get_gender(match.group("article"))
    plural = get_plural(match.group("plural"))
    return YiddishNoun(match.group("word"), gender, plural)


def parse_preposition(info):
    """
    Parse prepositions
    """
    return YiddishPreposition(info)


def parse_verb(info):
    """
    Parse verbs
    """
    info = info.replace("*", "")  # not sure about the meaning of *
    if "[" not in info:
        return YiddishVerb(info, None)
    info = info.replace("]", "")
    info = [x.strip() for x in info.split("[", 1)]
    return YiddishVerb(*info)


parse_func = {
    "adj": parse_adjective,
    "adv": parse_adverb,
    "interj": parse_interjection,
    "konj": parse_conjunction,
    "prep": parse_preposition,
    "s": parse_noun,
    "vb": parse_verb,
}


def parse_word(entry):
    """
    Parse JSON data according to the word type
    """
    return parse_func[get_graminfo(entry)](get_yiddish(entry))


def get_words(data):
    """
    Get all words in proper Python data structure
    """
    for entry in data:
        if get_graminfo(entry) not in parse_func:
            continue
        yield parse_word(entry)


def get_adjectives(words):
    """
    Get all adjectives
    """
    return filter(lambda x: isinstance(x, YiddishAdjective), words)


def get_adverbs(words):
    """
    Get all adverbs
    """
    return filter(lambda x: isinstance(x, YiddishAdverb), words)


def get_conjunctions(words):
    """
    Get all conjuntions
    """
    return filter(lambda x: isinstance(x, YiddishConjunction), words)


def get_interjections(words):
    """
    Get all interjections
    """
    return filter(lambda x: isinstance(x, YiddishInterjection), words)


def get_nouns(words):
    """
    Get all nouns
    """
    return filter(lambda x: isinstance(x, YiddishNoun), words)


def get_prepositions(words):
    """
    Get all prepositions
    """
    return filter(lambda x: isinstance(x, YiddishPreposition), words)


def get_verbs(words):
    """
    Get all verbs
    """
    return filter(lambda x: isinstance(x, YiddishVerb), words)
