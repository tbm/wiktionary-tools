# Copyright (C) 2024  Martin Michlmayr <tbm@cyrius.com>
# License: GNU General Public License (GPL), version 3 or above
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Functions related to hyphenation patterns
"""

__license__ = "GPL-3.0-or-later"

import re
import string
import unicodedata

import mwparserfromhell


def get_hyphenations(entry):
    """
    Extract hyphenation patterns from a Wiktionary entry.
    """
    for line in entry.splitlines(keepends=True):
        # This is just a speed optimization over calling mwparserfromhell
        # on the whole entry
        if not re.search(r"\{\{(hyph|es-pr|it-pr|fi-p|pl-p)", line):
            continue
        wikicode = mwparserfromhell.parse(line)
        for template in wikicode.filter_templates():
            if template.name in ("hyph", "hyphenation"):
                hyph = "|".join(str(p) for p in template.params[1:] if not p.showkey)
                for pattern in hyph.split("||"):
                    yield pattern.split("|")
            elif template.name in ("es-pr", "it-pr") and template.params:
                if match := re.search("<hyph:([^+-][^>]+)>", str(template.params[0])):
                    for hyph in re.split(r",\s*", match.group(1)):
                        yield hyph.split(".")
            elif template.name in ("fi-p", "fi-pronunciation", "pl-p"):
                for param in template.params:
                    if param.value.strip() == "-":
                        continue
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


def strip_punctuation(text):
    """
    Strip punctuation from a string
    """
    translation_table = str.maketrans("", "", string.punctuation)
    return text.translate(translation_table)


class Hyphenation:
    """
    Class for hyphenations
    """

    def __init__(self, word, hyph, lang=None):
        self.word = word
        self.hyph = hyph
        self.lang = lang
        self.hyph_str = "".join(self.hyph)

    def get_word(self):
        """
        Return the word
        """
        return self.word

    def get_hyph(self):
        """
        Return the hyphenation pattern (a list)
        """
        return self.hyph

    def __str__(self):
        return self.word + ": " + "·".join(self.hyph)

    def __eq__(self, other):
        if isinstance(other, Hyphenation):
            return self.word == other.word and self.hyph == other.hyph
        return False

    @classmethod
    def create(cls, word, hyph, lang):
        """
        Instantiate the right subclass depending on the language
        """
        lang_subclasses = {
            "ca": HyphenationCA,
            "de": HyphenationDE,
            "hu": HyphenationHU,
            "it": HyphenationIT,
            "nl": HyphenationNL,
            "sq": HyphenationSQ,
            "yi": HyphenationYI,
        }
        subclass = lang_subclasses.get(lang, cls)
        return subclass(word, hyph, lang)

    def is_valid(self):
        """
        Check if a hyphenation pattern matches the word
        """
        if self.word == self.hyph_str:
            return True
        # It's not clear what to do about hyphens, so accept this for now
        if self.word.replace("-", "") == self.hyph_str:
            return True
        # Spaces are not handled uniformly, so let's ignore them for now
        if self.word.replace(" ", "") == self.hyph_str.replace(" ", ""):
            return True
        # Ignore certain characters
        if strip_punctuation(self.word) == strip_punctuation(self.hyph_str):
            return True
        # Some language-specific rules
        if self.lang == "el":
            # Workaround: Greek uses separate hyph templates when a phrase
            # contains multiple words; pending discussion on how to handle
            # that, accept the pattern if it matches one of the words.
            if self.hyph_str in self.word.split(" "):
                return True
        return False


class HyphenationCA(Hyphenation):
    """
    Hyphenation module for Catalan
    """

    def is_valid(self):
        if super().is_valid():
            return True
        if self.word.replace("·", "") == self.hyph_str:
            return True
        return False


class HyphenationDE(Hyphenation):
    """
    Hyphenation module for German
    """

    def is_valid(self):
        if super().is_valid():
            return True
        # Pre German orthography reform of 1996, "ck" became "kk"
        if self.word == "".join(convert_german_kk_to_ck(self.hyph)):
            return True
        unusual_hyph = {
            "dämmrig": "dämmerig",
            "Brennessel": "Brennnessel",
            "justiziabel": "justitiabel",
        }
        if unusual_hyph.get(self.word) == self.hyph_str:
            return True
        return False


class HyphenationHU(Hyphenation):
    """
    Hyphenation module for Hungarian
    """

    def is_valid(self):
        if super().is_valid():
            return True
        hu_replacements = {
            "ccs": "cscs",
            "ggy": "gygy",
            "lly": "lyly",
            "nny": "nyny",
            "ssz": "szsz",
            "tty": "tyty",
        }
        modified_word = self.word
        for orig, repl in hu_replacements.items():
            modified_word = modified_word.replace(orig, repl)
        if modified_word == self.hyph_str:
            return True
        return False


class HyphenationIT(Hyphenation):
    """
    Hyphenation module for Italian
    """

    def is_valid(self):
        if super().is_valid():
            return True
        if remove_diacritics(self.word) == remove_diacritics(self.hyph_str):
            return True
        return False


class HyphenationNL(Hyphenation):
    """
    Hyphenation module for Dutch
    """

    def is_valid(self):
        if super().is_valid():
            return True
        if remove_diacritics(self.word) == self.hyph_str:
            return True
        return False


class HyphenationSQ(Hyphenation):
    """
    Hyphenation module for Albanian
    """

    def is_valid(self):
        if super().is_valid():
            return True
        # It seems the hyphenations have more diacritics than the
        # original word
        if remove_diacritics(self.word) == remove_diacritics(self.hyph_str):
            return True
        return False


class HyphenationYI(Hyphenation):
    """
    Hyphenation module for Yiddish
    """

    def is_valid(self):
        if super().is_valid():
            return True
        if self.word.replace("־", "") == self.hyph_str:
            return True
        return False
