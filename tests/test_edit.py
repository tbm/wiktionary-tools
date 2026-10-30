# Copyright (C) 2026  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for kamusi.edit functions
"""

import pytest

from kamusi.edit import add_category, add_ety_ref, add_thumbnail, add_wikipedia
from helpers import read_test

def test_add_category():
    """
    Basic test of test_add_category()
    """
    before = "==Swahili==\n===Noun===\n# test\n\n"
    after = "==Swahili==\n===Noun===\n# test\n\n{{C|sw|People}}\n\n"
    assert add_category(before, "People", "sw") == after

def test_add_category_already_present():
    """
    Test when a category exists already.
    """
    text = "==Swahili==\n# test\n\n{{C|sw|Occupations}}\n\n"
    assert add_category(text, "People", "sw") == text

def test_add_ety_ref_basic():
    """
    Basic test of add_ety_ref()
    """
    ref = "<ref>{{R:sw:Ref}}</ref>"
    before, after = read_test("add_ety_ref", "basic")
    assert add_ety_ref(before, ref) == after

def test_add_ety_ref_no_etymology():
    """
    Test without Etymology section
    """
    ref = "<ref>{{R:sw:Ref}}</ref>"
    text = ""
    with pytest.raises(ValueError, match="Can't find etymology header"):
        add_ety_ref(text, ref)

def test_add_ety_ref_not_right_etymology():
    """
    Test without the right Etymology section
    """
    ref = "<ref>{{R:sw:Ref}}</ref>"
    text = "===Etymology 1==="
    with pytest.raises(ValueError, match="Can't find etymology header"):
        add_ety_ref(text, ref, 2)

def test_add_ety_ref_ref_in_ety2():
    """
    Test when there's a reference in the following etymology
    """
    ref = "<ref>{{R:sw:Ref}}</ref>"
    before, after = read_test("add_ety_ref", "ref_in_ety2")
    assert add_ety_ref(before, ref, 1) == after

def test_add_thumbnail():
    """
    Test with image.jpg
    """
    before = "==Swahili==\n\n===Etymology===\n"
    thumbnail = "image.jpg"
    after = "==Swahili==\n[[File:image.jpg|thumb]]\n\n===Etymology===\n"
    assert add_thumbnail(before, thumbnail) == after

def test_add_thumbnail_file():
    """
    Test with File:image.jpg
    """
    before = "==Swahili==\n\n===Etymology===\n"
    thumbnail = "File:image.jpg"
    after = "==Swahili==\n[[File:image.jpg|thumb]]\n\n===Etymology===\n"
    assert add_thumbnail(before, thumbnail) == after

def test_add_thumbnail_description():
    """
    Test add_thumbnail() with description
    """
    before = "==Swahili==\n\n===Etymology===\n"
    thumbnail = "image.jpg"
    desc = "foo"
    after = "==Swahili==\n[[File:image.jpg|thumb|foo]]\n\n===Etymology===\n"
    assert add_thumbnail(before, thumbnail, desc) == after

def test_add_thumbnail_has_file():
    """
    Test add_thumbnail() when it has "File:" already
    """
    before = "==Swahili==\n[[File:image.jpg]]\n===Etymology===\n"
    assert add_thumbnail(before, "") == before

def test_add_thumbnail_has_image():
    """
    Test add_thumbnail() when it has "Image:" already
    """
    before = "==Swahili==\n[[Image:image.jpg]]\n===Etymology===\n"
    assert add_thumbnail(before, "") == before

def test_add_wikipedia():
    """
    Test of add_wikipedia()
    """
    before = "==Swahili==\n\n===Etymology===\n"
    after = "==Swahili==\n{{wp|sw:}}\n\n===Etymology===\n"
    assert add_wikipedia(before, "sw") == after

def test_add_wikipedia_has_wikipedia():
    """
    Test of add_wikipedia(): has {{wikipedia}} already
    """
    before = "==Swahili==\n{{wikipedia}}\n"
    assert add_wikipedia(before, "") == before

def test_add_wikipedia_has_wp():
    """
    Test of add_wikipedia(): has {{wp}} already
    """
    before = "==Swahili==\n{{wikipedia}}\n"
    assert add_wikipedia(before, "") == before
