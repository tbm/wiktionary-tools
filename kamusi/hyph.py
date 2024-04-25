"""
Functions related to hyphenation patterns
"""

import mwparserfromhell


def get_hyphenations(entry):
    """
    Extract hyphenation patterns from a Wiktionary entry.
    """
    for line in entry.splitlines(keepends=True):
        # This is just a speed optimization over calling mwparserfromhell
        # on the whole entry
        if not "{{hyph" in line and not "{{pl-p" in line:
            continue
        wikicode = mwparserfromhell.parse(line)
        for template in wikicode.filter_templates():
            if template.name in ("hyph", "hyphenation"):
                hyph = "|".join(str(p) for p in template.params[1:] if not p.showkey)
                for pattern in hyph.split("||"):
                    yield pattern
            elif template.name == "pl-p":
                for param in template.params:
                    if param.name.strip() in ("h", "h1", "h2", "h3"):
                        yield param.value.strip().replace(".", "|")
