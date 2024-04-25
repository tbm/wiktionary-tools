"""
Functions related to saving pages
"""

import kamusi


def format_changelog(lang, description):
    """
    Add the language to a description to generate a changelog
    """
    return "/* " + kamusi.code_to_name(lang) + " */ " + description
