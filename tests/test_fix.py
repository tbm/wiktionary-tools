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
        if templ in kamusi.fix.LANGCODE_TEMPLATES_IGNORE:
            continue
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


def test_fix_lang_code_param_number():
    """
    Test fix_lang_code(): test for 1=langcode syntax
    """
    before = "{{compound|1=de|2=hinweg|3=trösten}}"
    assert fix_lang_code(before, "de") == before


def test_fix_lang_code_newline():
    """
    Test fix_lang_code(): test for newline in value
    """
    before = "{{col|da\n|foo\n|bar\n}}"
    after = "{{col|de\n|foo\n|bar\n}}"
    assert fix_lang_code(before, "de") == after


def test_fix_lang_code_comment():
    """
    Test fix_lang_code(): test for comment in value
    """
    before = "{{col|da<!--foo-->\n|foo\n|bar\n}}"
    after = "{{col|de<!--foo-->\n|foo\n|bar\n}}"
    assert fix_lang_code(before, "de") == after


def test_fix_lang_code_comment_with_lang_code():
    """
    Test fix_lang_code(): test for comment containg old lang code in value
    """
    before = "{{col|da<!--lang code da here-->\n|foo\n|bar\n}}"
    after = "{{col|de<!--lang code da here-->\n|foo\n|bar\n}}"
    assert fix_lang_code(before, "de") == after


def test_fix_lang_code_nocat():
    """
    Test fix_lang_code(): test for nocat=1
    """
    before = "{{af|da|foo|bar|nocat=1}}"
    assert fix_lang_code(before, "de") == before


def test_fix_lang_code_lang():
    """
    Test fix_lang_code(): "lang" is used to refer to other languages
    """
    before = "{{lang|sw|moja}}"
    assert fix_lang_code(before, "de") == before


def test_fix_lang_code_lang_whitespace():
    """
    Test fix_lang_code(): check for whitespace in parameter 0
    """
    before = "{{ lang |sw|moja}}"
    assert fix_lang_code(before, "de") == before


def test_fix_lang_code_attention():
    """
    Test fix_lang_code(): "attention" is used to refer to other languages
    """
    before = "{{attention|sw|is this right?}}"
    assert fix_lang_code(before, "de") == before


def test_fix_lang_code_surf():
    """
    Test fix_lang_code(): "surf" allows special + syntax
    """
    before = "{{surf|+com|sw|foo|bar}}"
    after = "{{surf|+com|de|foo|bar}}"
    assert fix_lang_code(before, "de") == after


def test_fix_lang_code_surface_etymology():
    """
    Test fix_lang_code(): "surface etymology" allows special + syntax
    """
    before = "{{surface etymology|+com|sw|foo|bar}}"
    after = "{{surface etymology|+com|de|foo|bar}}"
    assert fix_lang_code(before, "de") == after


def test_fix_lang_code_surface_analysis():
    """
    Test fix_lang_code(): "surface analysis" allows special + syntax
    """
    before = "{{surface analysis|+com|sw|foo|bar}}"
    after = "{{surface analysis|+com|de|foo|bar}}"
    assert fix_lang_code(before, "de") == after


def test_fix_lang_code_surface_analysis_test_empty_parameter1():
    """
    Test fix_lang_code(): test for no parameter 1
    """
    before = "{{surface analysis}}"
    assert fix_lang_code(before, "de") == before


def test_fix_lang_code_quote_termlang():
    """
    Test fix_lang_code(): ignore if param "termlang" exists
    """
    before = "{{quote-journal|en|termlang=fr|...}}"
    assert fix_lang_code(before, "de") == before


def test_fix_lang_code_quote_multiple_lang_code():
    """
    Test fix_lang_code(): "quote" with multiple plan language codes
    """
    before = "{{quote-journal|en,fr, es|...}}"
    assert fix_lang_code(before, "de") == before


def test_fix_lang_code_cite_multiple_lang_code():
    """
    Test fix_lang_code(): "cite" with multiple plan language codes
    """
    before = "{{cite-web|en,fr, es|...}}"
    assert fix_lang_code(before, "de") == before
