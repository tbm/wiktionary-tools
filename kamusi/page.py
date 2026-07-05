"""
Wiktionary Page Abstraction
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Iterator
from dataclasses import dataclass
import re

from mwparserfromhell.nodes import Template
import pywikibot
import mwparserfromhell
from mwparserfromhell.wikicode import Wikicode
from mediawiki_langcodes import name_to_code

# import kamusi


class WiktionaryEntry:
    """
    Represents a language entry in a Wiktionary page.
    """
    def __init__(self, lang_code: str, content: str) -> None:
        self.lang_code = lang_code
        self.content = mwparserfromhell.parse(content)
        # self.etymology_sections = self._parse_etymology_sections()

    def __str__(self):
        return str(self.content)

    def add_section(self, header: str, content: str, level: int = 3) -> None:
        """
        Add a new section to the entry.
        """
        new_section = f"\n{'=' * level} {header} {'=' * level}\n{content}"
        self.content.append(new_section)

    def get_sections(self, header: str) -> List[Wikicode]:
        """
        Get content of a specific section within the entry.
        """
        return self.content.get_sections(levels=None, matches=f"^{header}$")

    # Should move these to part-of-speech section class.
    @property
    def definitions(self):
        pass

    @definitions.setter
    def definitions(self):
        pass


class EnglishWiktionaryEntry(WiktionaryEntry):
    """
    Entry class for English Wiktionary
    """

class GermanWiktionaryEntry(WiktionaryEntry):
    """
    Entry class for German Wiktionary
    """

class SwahiliWiktionaryEntry(WiktionaryEntry):
    """
    Entry class for Swahili Wiktionary
    """

    def __str__(self):
        header = "=={{" + self.lang_code + "}}==\n"
        return header + self.content.rstrip("\n") + "\n"

    def get_translations(self):
        """
        Yield translations from a page
        """
        trans = self.get_section("Tafsiri")
        if not trans:
            return
        for line in trans.splitlines():
            if match := re.match(r"\*\s*\{\{(\w+)\}\}\s*:\s*(.*)", line):
                yield match.groups()

class EtymologySection:
    """Base class for an etymology section, considered the top-level
    subdivision of a language entry. Some Wiktionaries have a flat
    layout, where there is at most 1 etymology section that explains
    all the senses, in which case there will be only one EtymologySection."""

    def __init__(self, site_code: str, etymology_section: Wikicode, content: Wikicode) -> None:
        self.etymology_section = etymology_section
        # self.pos_factory = {"en": EnglishPartOfSpeech, "sw": SwahiliPartOfSpeech}[site_code]
        self.pos_sections = self._parse_pos_sections()

    def _parse_pos_sections(self) -> None:
        # for section in self.content.get_sections():
            pass

class MultipleAlsoError(ValueError):
    """Error class representing a case where more than one
    see-also template at the beginning of the page is encountered.
    This is not supposed to be present, so catch it if it occurs."""
    pass

# May need to go in another module, but put here for now.
def get_prelude(page_content: Wikicode) -> Wikicode:
    """Return all Wikicode preceding the first language
    section in the page."""
    return Wikicode(page_content.nodes[:page_content.index(
        page_content.get_sections([2])[0].nodes[0]
    )])

class Also:
    ALSO_TEMPLATES = {"en": "also", "de": "Siehe auch"}

    def _get_also_pattern(self, also_template_name: str) -> str:
        return rf"^{{{{{also_template_name}\|.*}}}}$"

    def _parse_also(self, content: Wikicode, also_pattern: str) -> List[Template]:
        return content.filter_templates(matches=also_pattern)

    def __init__(self, site_code: str, page_content: Wikicode):
        self.site_code = site_code

        also_template_name = self.ALSO_TEMPLATES.get(site_code)
        if also_template_name is None:
            return

        also_pattern = self._get_also_pattern(also_template_name)
        also_templates = self._parse_also(page_content, also_pattern)

        if len(also_templates) == 0:
            return
        elif len(also_templates) > 1:
            raise MultipleAlsoError(also_templates, "Page has more than 1 also template.")
        self._also = also_templates[0]

        # Error checking ‒ redundant?
        prelude = get_prelude(page_content)
        if self._parse_also(prelude, also_pattern) != also_templates:
            raise ValueError("Misplaced also template (not at beginning of page)", page_content)

    def __repr__(self) -> str:
        return str(self.get())

    def __del__(self) -> None:
        self._also = None

    def get(self) -> List[str]:
        if self._also is None:
            return []

        if self.site_code == "en":
            return [str(param.value) for param in self._also.params if param.name.isdigit()]
        elif self.site_code == "de":
            if not self._also.has("1"):
                return []
            return [re.sub(r"[\[\]]", "", x) for x in str(self._also.get("1")).split(", ")]
        else:
            return []

    def set(self, value: List[str]) -> None:
        if self._also is None:
            return

        if self.site_code == "de":
            self._also.add("1", ", ".join(f"[[{x}]]" for x in value))
        elif self.site_code == "en":
            existing = [param.value for param in self._also.params if param.name.isdigit()]
            current_index = len(existing)
            # Remove all numeric template parameters and re-add them.
            for i in range(current_index):
                self._also.remove(str(i+1))
            for i, also in enumerate(value):
                self._also.add(str(i+1), also)

    def add(self, also: str) -> None:
        self.set(self.get() + [also])

    def wikicode(self) -> Optional[Template]:
        return self._also

class WiktionaryPage(ABC):
    """
    Base class for Wiktionary pages across different language editions.
    """

    def __init__(self, title: str, site_lang: str):
        self.title = title
        self.site_lang = site_lang
        self.site = self._get_default_site()
        self.page = pywikibot.Page(self.site, title)
        self._parsed = mwparserfromhell.parse(self.page.text)
        self._also = Also(site_lang, self._parsed)
        self.entries: List[WiktionaryEntry] = []

        self.entry_factory = {
            "en": EnglishWiktionaryEntry,
            "sw": SwahiliWiktionaryEntry,
            "de": GermanWiktionaryEntry,
        }[site_lang]

        if self.page.exists():
            self._parse_page()

    def __repr__(self) -> str:
        # Use the parsed representation to get a reliable string form.
        return str(self._parsed)

    def _get_default_site(self) -> pywikibot.site.APISite:
        """
        Return the default site for this Wiktionary edition.
        """
        return pywikibot.Site(self.site_lang, "wiktionary")

    @abstractmethod
    def _get_language_sort_key(self, lang_code: str) -> int:
        """
        Return sort priority for a given language. Lower values come first.
        """

    @abstractmethod
    def _format_also(self, also: List[str]) -> str:
        """
        Format "also" links according to this Wiktionary's conventions.
        """

    def _map_lang(self, lang: str) -> str:
        if lang.startswith("{{"):
            return lang.strip("{}")
        return name_to_code(lang)

    def _parse_page(self) -> None:
        """
        Parse the page content into also links and language entries.
        """
        for language_entry in self._parsed.get_sections([2]):
            self.entries.append(self.entry_factory(self.site_lang, language_entry))

    def _sort_entries(self) -> None:
        """
        Sort entries based on language priority and alphabetically.
        """
        # TODO

    def add_entry(self, entry: WiktionaryEntry) -> None:
        """
        Add a new language entry to the page.
        """
        # Remove entry with same language
        self.entries = [cur for cur in self.entries if cur.lang_code != entry.lang_code]
        self.entries.append(entry)
        self._sort_entries()

    def get_entries(self) -> List[WiktionaryEntry]:
        """
        Return entries
        """
        return list(self.entries)

    def iter_entries(self) -> Iterator[WiktionaryEntry]:
        """
        Iterate over entries
        """
        for entry in self.entries:
            yield entry

    def get_entry(self, lang_code: str) -> Optional[WiktionaryEntry]:
        """
        Get a specific language entry.
        """
        for entry in self.entries:
            if entry.lang_code == lang_code:
                return entry
        return None

    def get_text(self) -> str:
        """
        Return text of entry
        """
        return str(self)

    @property
    def also(self) -> List[str]:
        return self._also.get()

    @also.setter
    def also(self, alsos: List[str]) -> None:
        self._also.set(alsos)

    @also.deleter
    def also(self) -> None:
        wikicode = self._also.wikicode()
        if wikicode is None:
            return
        self._parsed.remove(wikicode)
        del self._also
        i = 0
        while i < len(self._parsed.nodes) and not isinstance(self._parsed.nodes[i], mwparserfromhell.nodes.heading.Heading):
            if self._parsed.nodes[i].isspace():
                self._parsed.nodes.pop(i)
            else:
                i += 1

    def add_also(self, link: str) -> None:
        """
        Add a new "also" link.
        """
        self._also.add(link)

    def save(self, summary: Optional[str] = None, minor=False) -> None:
        """
        Save the page back to Wiktionary.
        """
        self.page.text = self.get_text()
        self.page.save(summary=summary, minor=minor)


class EnglishWiktionaryPage(WiktionaryPage):
    """
    Implementation for English Wiktionary.
    """

    def _get_language_sort_key(self, lang_code: str) -> int:
        priority_map = {"mul": 0, "en": 1}
        return priority_map.get(lang_code, 999)

    def _format_also(self, also: List[str]) -> str:
        return "{{also|" + "|".join(also) + "}}\n"

class GermanWiktionaryPage(WiktionaryPage):
    """
    Implementation for German Wiktionary.
    """

    def _get_language_sort_key(self, lang_code: str) -> int:
        priority_map = {"de": 0}
        return priority_map.get(lang_code, 999)

    # Not needed anymore, but will clean later.
    def _format_also(self, also: List[str]) -> str:
        return "{{Siehe auch|" + "|".join(also) + "}}\n"

class SwahiliWiktionaryPage(WiktionaryPage):
    """
    Implementation for Swahili Wiktionary.
    """

    def _get_language_sort_key(self, lang_code: str) -> int:
        priority_map = {
            "sw": 1,
        }
        return priority_map.get(lang_code, 999)

    def _format_also(self, also: List[str]) -> str:
        return ""
