# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Test ISOF Swedish-Yiddish dictionary parsing
"""

__license__ = "GPL-3.0-or-later"

from isofyi import get_gender, get_plural
from isofyi import parse_adjective, YiddishAdjective
from isofyi import parse_adverb, YiddishAdverb
from isofyi import parse_conjunction, YiddishConjunction
from isofyi import parse_interjection, YiddishInterjection
from isofyi import parse_noun, YiddishNoun
from isofyi import parse_preposition, YiddishPreposition
from isofyi import parse_verb, YiddishVerb


def test_get_article():
    """
    Tests for article -> gender
    """
    assert get_gender("דער") == "m"
    assert get_gender("די") == "f"
    assert get_gender("דאָס") == "n"
    assert get_gender("דער/די") == "mf"
    assert get_gender("דער/דאָס") == "mn"
    assert get_gender("דאָס/די") == "fn"
    assert get_gender("די/דער") == "mf"
    assert get_gender("דאָס/דער") == "mn"
    assert get_gender("די/דאָס") == "fn"
    assert get_gender("די\\דאָס") == "fn"
    assert get_gender("דער\\די") == "mf"


def test_get_plural():
    """
    Tests for plural endings
    """
    assert get_plural("־ען") == "en"
    assert get_plural("־ער") == "er"
    assert get_plural("־עס") == "es"
    assert get_plural("־ן") == "n"
    assert get_plural("־ס") == "s"
    assert get_plural("־ים") == "im"
    assert get_plural("־עך") == "ech"


def test_parse_adjective():
    """
    Tests for adjective parsing
    """
    assert parse_adjective("פֿרײַנדלעך") == YiddishAdjective("פֿרײַנדלעך")


def test_parse_adverb():
    """
    Tests for adverb parsing
    """
    assert parse_adverb("טאַקע") == YiddishAdverb("טאַקע")


def test_parse_conjunction():
    """
    Tests for conjunction parsing
    """
    assert parse_conjunction("הגם") == YiddishConjunction("הגם")


def test_parse_interjection():
    """
    Tests for interjection parsing
    """
    assert parse_interjection("בראַוואָ!") == YiddishInterjection("בראַוואָ")
    assert parse_interjection("אַדיע") == YiddishInterjection("אַדיע")


def test_parse_noun():
    """
    Tests for noun parsing
    """
    assert parse_noun("אינדזל, דער [־ען]") == YiddishNoun("אינדזל", "m", "en")
    assert parse_noun("צדקה, די") == YiddishNoun("צדקה", "f", None)


def test_parse_preposition():
    """
    Tests for preposition parsing
    """
    assert parse_preposition("פֿון") == YiddishPreposition("פֿון")


def test_parse_verb():
    """
    Tests for verb parsing
    """
    assert parse_verb("קושן [געקושט]") == YiddishVerb("קושן", "געקושט")
    assert parse_verb("אָפּלויפֿן* [אָפּגעלאָפֿן]") == YiddishVerb(
        "אָפּלויפֿן", "אָפּגעלאָפֿן"
    )
    assert parse_verb("זײַן") == YiddishVerb("זײַן", None)
