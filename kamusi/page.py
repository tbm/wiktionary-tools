"""
Wiktionary Page Abstraction
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Iterator
from dataclasses import dataclass
import re

import pywikibot
from mediawiki_langcodes import name_to_code

import kamusi


@dataclass
class WiktionaryEntry:
    """
    Represents a language entry in a Wiktionary page.
    """

    lang_code: str
    content: str

    def __str__(self):
        header = f"=={kamusi.code_to_name(self.lang_code)}==\n"
        return header + self.content.rstrip("\n") + "\n"

    def add_section(self, header: str, content: str, level: int = 3) -> None:
        """
        Add a new section to the entry.
        """
        new_section = f"\n{'=' * level} {header} {'=' * level}\n{content}"
        self.content += new_section

    def get_section(self, header: str) -> Optional[str]:
        """
        Get content of a specific section within the entry.
        """
        sections = self._parse_sections()
        return sections.get(header)

    def _parse_sections(self) -> Dict[str, str]:
        """
        Parse the entry content into a dictionary of section header -> content.
        """
        sections = {}
        current_section = None
        current_content = []

        for line in self.content.split("\n"):
            if line.startswith("="):
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                    current_content = []
                current_section = line.strip("= ")
            else:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections


class EnglishWiktionaryEntry(WiktionaryEntry):
    """
    Entry class for English Wiktionary
    """

    def __str__(self):
        header = f"=={kamusi.code_to_name(self.lang_code)}==\n"
        return header + self.content.rstrip("\n") + "\n"


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


class WiktionaryPage(ABC):
    """
    Base class for Wiktionary pages across different language editions.
    """

    def __init__(self, title: str, site_lang: str):
        self.title = title
        self.site_lang = site_lang
        self.site = self._get_default_site()
        self.page = pywikibot.Page(self.site, title)
        self.also: List[str] = []
        self.entries: List[WiktionaryEntry] = []

        self.entry_factory = {
            "en": EnglishWiktionaryEntry,
            "sw": SwahiliWiktionaryEntry,
        }[site_lang]

        if self.page.exists():
            self._parse_page()

    def __str__(self) -> str:
        text = ""
        if self.also:
            text += self._format_also(self.also)
        text += "\n".join(str(entry) for entry in self.entries)
        return text

    def _get_default_site(self) -> pywikibot.Site:
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
        content = self.page.text
        current_language = None
        current_content = []

        for line in content.split("\n"):
            # Check for "See also" section
            if line.startswith("{{also"):
                self.also = line[7:].rstrip("}").split("|")
            elif line.startswith("==") and not line.startswith("==="):
                # New language section
                if current_language:
                    self.entries.append(
                        self.entry_factory(
                            self._map_lang(current_language), "\n".join(current_content)
                        )
                    )
                current_content = []
                current_language = line.strip("= ")
            else:
                current_content.append(line)

        # Handle last section
        if current_language:
            self.entries.append(
                self.entry_factory(
                    self._map_lang(current_language), "\n".join(current_content)
                )
            )

        self._sort_entries()

    def _sort_entries(self) -> None:
        """
        Sort entries based on language priority and alphabetically.
        """
        self.entries.sort(
            key=lambda entry: (
                self._get_language_sort_key(entry.lang_code),
                kamusi.code_to_name(entry.lang_code, self.site_lang),
            )
        )

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

    def add_also(self, link: str) -> None:
        """
        Add a new "also" link.
        """
        if link not in self.also:
            self.also.append(link)

    def save(self, summary: str = None, minor=False) -> None:
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
