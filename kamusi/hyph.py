"""
Functions related to hyphenation patterns
"""

import unicodedata

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
                    yield pattern.split("|")
            elif template.name == "pl-p":
                for param in template.params:
                    if param.name.strip() in ("h", "h1", "h2", "h3"):
                        yield param.value.strip().split(".")


def convert_german_kk_to_ck(hyph):
    """
    Pre the German orthography reform of 1996, "ck" became "kk" during
    hyphenation.  Let's change the "kk" back to "ck" so we can compare
    the hyphenation pattern with the original word.
    """
    result = []
    # If both current and next word starts/ends with 'k', replace it with 'c' in current word
    for i, word in enumerate(hyph):
        if i < len(hyph) - 1 and hyph[i].endswith("k") and hyph[i + 1].startswith("k"):
            word = word[:-1] + "c"
        result.append(word)
    return result


def remove_diacritics(text):
    """
    Remove diacritics from a string
    """
    norm_text = unicodedata.normalize("NFD", text)
    shaved = "".join(c for c in norm_text if not unicodedata.combining(c))
    return unicodedata.normalize("NFC", shaved)


class Hyphenation:
    """
    Class for hyphenations
    """

    def __init__(self, word, hyph, lang=None):
        self.word = word
        self.hyph = hyph
        self.lang = lang

    def get_word(self):
        """
        Return the word
        """
        return self.word

    def get_hyph(self):
        """
        Return the hypenation pattern (a list)
        """
        return self.hyph

    def __str__(self):
        return self.word + ": " + "·".join(self.hyph)

    def __eq__(self, other):
        if isinstance(other, Hyphenation):
            return self.word == other.word and self.hyph == other.hyph
        return False

    def is_valid(self):
        """
        Check if a hyphenation pattern matches the word
        """
        if self.word == "".join(self.hyph):
            return True
        # It's not clear what to do about hyphens, so accept this for now
        if self.word.replace("-", "") == "".join(self.hyph):
            return True
        # Spaces are not handled uniformly, so let's ignore them for now
        if self.word.replace(" ", "") == "".join(self.hyph).replace(" ", ""):
            return True
        # Ignore certain characters
        if self.word.replace(",", "") == "".join(self.hyph):
            return True
        if self.word.replace(", ", "") == "".join(self.hyph):
            return True
        if self.word.replace("'", "") == "".join(self.hyph):
            return True
        # Some language-specific rules
        if self.lang == "ca":
            if self.word.replace("·", "") == "".join(self.hyph):
                return True
        elif self.lang == "de":
            # Pre German orthography reform of 1996, "ck" became "kk"
            if self.word == "".join(convert_german_kk_to_ck(self.hyph)):
                return True
        elif self.lang == "nl":
            if remove_diacritics(self.word) == "".join(self.hyph):
                return True
        elif self.lang == "yi":
            if self.word.replace("־", "") == "".join(self.hyph):
                return True
        return False
