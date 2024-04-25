"""
Functions related to languages and language codes.
"""

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
