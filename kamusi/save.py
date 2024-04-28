# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Functions related to saving pages
"""

__license__ = "GPL-3.0-or-later"

import kamusi


def format_changelog(description, lang, site="en"):
    """
    Add the language to a description to generate a changelog
    """
    return "/* " + kamusi.code_to_name(lang, site) + " */ " + description
