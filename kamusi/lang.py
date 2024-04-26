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
    "lg": "Luganda",
    "mfe": "Mauritian Creole",
    "ny": "Chichewa",
    "pam": "Kapampangan",
}


def code_to_name(lang):
    """
    Map a language code to a language name.

    Unfortunately, code_to_name from mediawiki_langcodes returns some
    names which are different on Wiktionary, so we have some overrides.
    """
    return LANG_MAP.get(lang, mediawiki_langcodes.code_to_name(lang, "en"))
