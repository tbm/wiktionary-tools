"""
Edit Wiktionary pages
"""

def add_wikipedia(entry, lang):
    """
    Add Wikipedia link to  entry
    """
    if "{{wikipedia" in entry or "{{wp" in entry:
        return entry
    first_break = entry.find("\n\n") + 1
    wp = "{{wikipedia"
    if lang != "en":
        wp += "|lang=" + lang
    wp += "}}"
    return entry[:first_break] + wp + "\n" + entry[first_break:]
