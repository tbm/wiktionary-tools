# Copyright (C) 2026  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for kamusi.edit functions
"""

from pathlib import Path

DATA = Path(__file__).parent / "data"


def read_test(directory: str, test: str) -> tuple[str, str]:
    """
    Read test case consisting of "before" and "after" text
    """
    root = DATA / directory
    before = (root / f"{test}/before.wiki").read_text(encoding="utf-8")
    after = (root / f"{test}/after.wiki").read_text(encoding="utf-8")
    return before, after
