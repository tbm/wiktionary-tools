# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Test Yiddish functions (Swedish Wiktionary)
"""

__license__ = "GPL-3.0-or-later"

import mwparserfromhell

from kamusi.yi_sv import get_noun_section, get_gender, get_noun, get_verb
from isofyi import YiddishNoun, YiddishVerb

YI_SV_NOUN_1 = """==Jiddisch==
===Substantiv===
{{subst|yi}}
'''foo''' (foo)
"""

YI_SV_NOUN_2 = """==Jiddisch==
===Substantiv===
{{subst|yi}}
'''foo''' (foo)

===Verb===
"""

YI_SV_NOUN_3 = """==Jiddisch==
===Verb===
{{verb|yi}}
#[[...]

===Substantiv===
{{subst|yi}}
'''foo''' (foo)
"""


def test_get_noun_section():
    """
    Tests for get_noun_section()
    """
    yi_sv_noun_section = YI_SV_NOUN_1[13:]
    assert get_noun_section("") is None
    assert get_noun_section(YI_SV_NOUN_1) == yi_sv_noun_section
    assert get_noun_section(YI_SV_NOUN_2) == yi_sv_noun_section
    assert get_noun_section(YI_SV_NOUN_3) == yi_sv_noun_section


def test_get_gender():
    """
    Tests for get_gender()
    """

    def str2tmpl(string):
        wikicode = mwparserfromhell.parse(string)
        return wikicode.filter_templates()

    assert get_gender(str2tmpl("{{f}}")) == "f"
    assert get_gender(str2tmpl("{{m}}")) == "m"
    assert get_gender(str2tmpl("{{n}}")) == "n"

    assert get_gender(str2tmpl("{{fpl}}")) == "fp"
    assert get_gender(str2tmpl("{{mpl}}")) == "mp"
    assert get_gender(str2tmpl("{{npl}}")) == "np"

    # Tests for order
    assert get_gender(str2tmpl("{{m}} {{f}}")) == "mf"
    assert get_gender(str2tmpl("{{f}} {{m}}")) == "mf"
    assert get_gender(str2tmpl("{{m}} {{n}}")) == "mn"
    assert get_gender(str2tmpl("{{n}} {{m}}")) == "mn"
    assert get_gender(str2tmpl("{{f}} {{n}}")) == "fn"
    assert get_gender(str2tmpl("{{n}} {{f}}")) == "fn"
    assert get_gender(str2tmpl("{{m}} {{f}} {{n}}")) == "mfn"
    assert get_gender(str2tmpl("{{m}} {{n}} {{f}}")) == "mfn"
    assert get_gender(str2tmpl("{{f}} {{n}} {{m}}")) == "mfn"
    assert get_gender(str2tmpl("{{n}} {{f}} {{m}}")) == "mfn"


def test_get_noun_no_gender():
    """
    Test get_noun() with no gender
    """
    entry = """==Jiddisch==
===Substantiv===
{{subst|yi}}
'''foo''' (foo)
   """
    assert get_noun("Foo", entry) == YiddishNoun("Foo", None, None)


def test_get_noun_one_gender():
    """
    Test get_noun() with one gender
    """
    entry = """==Jiddisch==
===Substantiv===
{{subst|yi}}
'''foo''' (foo) {{m}}
   """
    assert get_noun("Foo", entry) == YiddishNoun("Foo", "m", None)


def test_get_noun_two_gender():
    """
    Test get_noun() with two genders
    """
    entry = """==Jiddisch==
===Substantiv===
{{subst|yi}}
'''foo''' (foo) {{m}} ''eller'' {{f}}
   """
    assert get_noun("Foo", entry) == YiddishNoun("Foo", "mf", None)


def test_get_verb():
    """
    Test get_verb()
    """
    entry = """==Jiddisch==
===Verb===
{{verb|yi}}
'''foo''' (foo)
#[[foo]]
   """
    assert get_verb("Foo", entry) == YiddishVerb("Foo", None)
