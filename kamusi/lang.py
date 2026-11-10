# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Functions related to languages and language codes.
"""

__license__ = "GPL-3.0-or-later"

import re

import mediawiki_langcodes

# Wiktionary-specific overrides
LANG_MAP = {
    "ilo": "Ilocano",
    "jam": "Jamaican Creole",
    "lg": "Luganda",
    "mfe": "Mauritian Creole",
    "mul": "Translingual",
    "ny": "Chichewa",
    "pam": "Kapampangan",
    "rw": "Rwanda-Rundi",
    "ss": "Swazi",
    "bnt-sab-pro": "Proto-Sabaki",
}

LANG_CODE = re.compile(r"([a-z]{2,3}(-[a-zA-Z]{2,3})?)")


def code_to_name(lang, site="en"):
    """
    Map a language code to a language name.

    Unfortunately, code_to_name from mediawiki_langcodes returns some
    names which are different on Wiktionary, so we have some overrides.
    """
    lang_name = LANG_MAP.get(lang, mediawiki_langcodes.code_to_name(lang, site))
    if site == "sv":
        return lang_name.title()
    return lang_name


def get_langcode(text):
    """
    Return language code from string
    """
    match = LANG_CODE.search(text)
    return match.group(1) if match else None
