# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Functions related to languages and language codes.
"""

__license__ = "GPL-3.0-or-later"

import mediawiki_langcodes

# Wiktionary-specific overrides
LANG_MAP = {
    "bcl": "Bikol Central",
    "ilo": "Ilocano",
    "jam": "Jamaican Creole",
    "lg": "Luganda",
    "mfe": "Mauritian Creole",
    "mul" :"Translingual",
    "ny": "Chichewa",
    "pam": "Kapampangan",
    "rw": "Rwanda-Rundi",
    "ss": "Swazi",
}


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
