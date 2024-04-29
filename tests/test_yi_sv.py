# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Test Yiddish functions (Swedish Wiktionary)
"""

__license__ = "GPL-3.0-or-later"

from kamusi.yi_sv import get_noun_section, get_noun, get_verb
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
