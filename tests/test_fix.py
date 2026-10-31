# Copyright (C) 2026  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for kamusi.fix functions
"""

from pathlib import Path

import kamusi.fix
from kamusi.fix import fix_lang_code

DATA = Path(__file__).parent / "data"


def test_fix_lang_code():
    """
    Test fix_lang_code(): fix lang code
    """
    before = "{{af|de|m-|pika|alt2=-pika|-aji}}"
    after = "{{af|sw|m-|pika|alt2=-pika|-aji}}"
    assert fix_lang_code(before, "sw") == after


def test_fix_lang_code_no_change():
    """
    Test fix_lang_code(): no change
    """
    before = "{{af|sw|m-|pika|alt2=-pika|-aji}}"
    assert fix_lang_code(before, "sw") == before


def test_fix_lang_code_inline_no_change():
    """
    Test fix_lang_code(): with named parameter before lang code
    """
    before = "{{ux|inline=1|sw|foo|bar}}"
    assert fix_lang_code(before, "sw") == before


def test_fix_lang_code_inline_change():
    """
    Test fix_lang_code(): with named parameter before lang code
    """
    before = "{{ux|inline=1|de|foo|bar}}"
    after = "{{ux|inline=1|sw|foo|bar}}"
    assert fix_lang_code(before, "sw") == after


def test_fix_lang_code_ety_id_no_change():
    """
    Test fix_lang_code(): with named parameter before lang code
    """
    before = "{{ety|id=proclamation|sw|:from|foo}}"
    assert fix_lang_code(before, "sw") == before


def test_fix_lang_code_ety_id_change():
    """
    Test fix_lang_code(): with named parameter before lang code
    """
    before = "{{ety|id=proclamation|de|:from|foo}}"
    after = "{{ety|id=proclamation|sw|:from|foo}}"
    assert fix_lang_code(before, "sw") == after


def test_fix_lang_code_all():
    """
    Test fix_lang_code(): test all templates
    """
    for templ in kamusi.fix.LANGCODE_TEMPLATES:
        before = "{{" + templ + "|de|...}}"
        after = "{{" + templ + "|sw|...}}"
        assert fix_lang_code(before, "sw") == after


def test_fix_lang_code_whitespace():
    """
    Test fix_lang_code(): whitespace around lang code
    """
    before = "{{af|sw |...}}"
    assert fix_lang_code(before, "sw") == before
    before = "{{af| sw|...}}"
    assert fix_lang_code(before, "sw") == before
    before = "{{af| sw |...}}"
    assert fix_lang_code(before, "sw") == before


def test_fix_lang_code_accept_mul():
    """
    Test fix_lang_code(): accept "mul" as lang code
    """
    before = "{{audio|mul|Near-open front unrounded vowel.ogg}}"
    assert fix_lang_code(before, "sw") == before
