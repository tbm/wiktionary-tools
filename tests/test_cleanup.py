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
    before = "{{suffixusex|sw|vaa|alt1=-vaa|t1=to wear|valisha|alt2=-valisha|t2=to dress}}"
    after = "{{suffixusex|sw|vaa<alt:-vaa><t:to wear>|valisha<alt:-valisha><t:to dress>}}"
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

def test_convert_inline_params_from_files():
    """
    Test convert_inline_params(): compare before and after from files
    """
    test_dir = DATA / "cleanup" / "inline"
    for path in test_dir.glob("before/*"):
        before = path.read_text(encoding="utf-8")
        after = (test_dir / "after" / path.stem).read_text(encoding="utf-8")
        assert convert_inline_params(before) == after
