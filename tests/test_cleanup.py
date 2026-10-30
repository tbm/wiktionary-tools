# Copyright (C) 2026  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for kamusi.cleanup functions
"""

from pathlib import Path

import pytest

from kamusi.cleanup import convert_inline_params
from helpers import read_test

DATA = Path(__file__).parent / "data"


def test_convert_inline_params_basic():
    """
    Basic test of convert_inline_params()
    """
    before = "{{af|sw|m-|pika|alt2=-pika|-aji}}"
    after = "{{af|sw|m-|pika<alt:-pika>|-aji}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_param_order():
    """
    Test convert_inline_params(): ensure param order doesn't matter
    """
    before = "{{af|sw|m-|pika|-aji|alt2=-pika}}"
    after = "{{af|sw|m-|pika<alt:-pika>|-aji}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_suffixusex():
    """
    Test convert_inline_params(): test suffixusex
    """
    before = "{{suffixusex|sw|vaa|alt1=-vaa|t1=to wear|valisha|alt2=-valisha}}"
    after = "{{suffixusex|sw|vaa<alt:-vaa><t:to wear>|valisha<alt:-valisha>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_alter():
    """
    Test convert_inline_params(): test alter
    """
    before = "{{alter|sw|rundika|alt1=-rundika}}"
    after = "{{alter|sw|rundika<alt:-rundika>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_syn():
    """
    Test convert_inline_params(): test syn
    """
    before = "{{syn|sw|a|b|qq1=aa|qq2=bb}}"
    after = "{{syn|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_lit():
    """
    Test convert_inline_params(): test &lit - inline syntax not supported
    """
    before = "{{&lit|sw|juu|a|alt2=ya}}"
    assert convert_inline_params(before) == before


def test_convert_inline_params_sw_der():
    """
    Test convert_inline_params(): test sw-der - don't convert
    """
    before = "{{sw-der|a|b|c|nom1=foo|nom2=bar}}"
    assert convert_inline_params(before) == before


def test_convert_inline_params_unnumbered_reduplication():
    """
    Test convert_inline_params(): test reduplication with unnumbered parameter
    """
    before = "{{reduplication|sw|foka|alt=-foka|gloss=to rap}}"
    after = "{{reduplication|sw|foka<alt:-foka><t:to rap>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_rdp():
    """
    Test convert_inline_params(): test rdp with unnumbered parameter
    """
    before = "{{rdp|sw|foka|alt=-foka|gloss=to rap}}"
    after = "{{rdp|sw|foka<alt:-foka><t:to rap>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_coordinate_terms():
    """
    Test convert_inline_params(): test coordinate terms with unnumbered parameter
    """
    before = "{{coordinate terms|sw|a|b|qq=aa|qq2=bb}}"
    after = "{{coordinate terms|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_coo():
    """
    Test convert_inline_params(): test coo with unnumbered parameter
    """
    before = "{{coo|sw|a|b|qq=aa|qq2=bb}}"
    after = "{{coo|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_coord():
    """
    Test convert_inline_params(): test coord with unnumbered parameter
    """
    before = "{{coord|sw|a|b|qq=aa|qq2=bb}}"
    after = "{{coord|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_cot():
    """
    Test convert_inline_params(): test cot with unnumbered parameter
    """
    before = "{{cot|sw|a|b|qq=aa|qq2=bb}}"
    after = "{{cot|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_redup():
    """
    Test convert_inline_params(): test redup with unnumbered parameter
    """
    before = "{{redup|sw|foka|alt=-foka|gloss=to rap}}"
    after = "{{redup|sw|foka<alt:-foka><t:to rap>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_synonyms():
    """
    Test convert_inline_params(): test synonyms with unnumbered parameter
    """
    before = "{{synonyms|sw|a|b|qq=aa|qq2=bb}}"
    after = "{{synonyms|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_syn():
    """
    Test convert_inline_params(): test syn with unnumbered parameter
    """
    before = "{{syn|sw|a|b|qq=aa|qq2=bb}}"
    after = "{{syn|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_antonyms():
    """
    Test convert_inline_params(): test antonyms with unnumbered parameter
    """
    before = "{{antonyms|sw|a|b|qq=aa|qq2=bb}}"
    after = "{{antonyms|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_antonym():
    """
    Test convert_inline_params(): test ant with unnumbered parameter
    """
    before = "{{antonym|sw|a|b|qq=aa|qq2=bb}}"
    after = "{{antonym|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_unnumbered_ant():
    """
    Test convert_inline_params(): test ant with unnumbered parameter
    """
    before = "{{ant|sw|a|b|qq=aa|qq2=bb}}"
    after = "{{ant|sw|a<qq:aa>|b<qq:bb>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_gloss():
    """
    Test convert_inline_params(): test gloss -> t
    """
    before = "{{af|sw|m-|pika|alt2=-pika|gloss2=to cook}}"
    after = "{{af|sw|m-|pika<alt:-pika><t:to cook>}}"
    assert convert_inline_params(before) == after


def test_convert_inline_params_from_files():
    """
    Test convert_inline_params(): compare before and after from files
    """
    test_dir = DATA / "cleanup" / "inline"
    for path in test_dir.glob("before/*"):
        before = path.read_text(encoding="utf-8")
        after = (test_dir / "after" / path.stem).read_text(encoding="utf-8")
        assert convert_inline_params(before) == after
