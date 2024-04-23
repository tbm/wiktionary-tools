"""
Functions related to saving pages
"""

from mediawiki_langcodes import code_to_name


def format_changelog(lang, description):
    """
    Add the language to a description to generate a changelog
    """
    return "/* " + code_to_name(lang, "en") + " */ " + description
