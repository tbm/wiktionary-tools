"""
Edit Wiktionary pages
"""

from .entry import get_entry


def add_wikipedia(text, lang):
    """
    Add Wikipedia link to text
    """
    text = get_entry(text, lang)
    if not text:
        return None
    if "{{wikipedia" in text or "{{wp" in text:
        return text
    first_break = text.find("\n\n") + 1
    wp = "{{wikipedia"
    if lang != "en":
        wp += "|lang=" + lang
    wp += "}}"
    return text[:first_break] + wp + "\n" + text[first_break:]
