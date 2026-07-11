from dataclasses import dataclass
from typing import Callable, Tuple
import kamusi
import unittest
import pathlib

from kamusi.page import WiktionaryPage

@dataclass
class WikicodeTestData:
    page_title: str
    before: str
    after: str

class KamusiTestCase(unittest.TestCase):
    def get_test_data(self, theme: str, case: str, before_name: str = "before.wiki", after_name = "after.wiki") -> WikicodeTestData:
        root = pathlib.Path("cases") / theme / case
        with open(root / "title") as f:
            title = f.read()
        with open(root / before_name) as f:
            before = f.read()
        with open(root / after_name) as f:
            after = f.read()
        return WikicodeTestData(title, before, after)

    def do_wikicode_test(self, test_data: WikicodeTestData, operation: Callable[[WikicodeTestData], WiktionaryPage]):
        page_final = operation(test_data)
        self.assertEqual(
            str(page_final),
            test_data.after
        )

class TestAlso(KamusiTestCase):
    def test_en_add(self):
        test_data = self.get_test_data("also", "en_add_new")

        def add_also(test_data):
            page = kamusi.EnglishWiktionaryPage(test_data.page_title, from_text=test_data.before)
            page.also = ["Hima"]
            return page

        self.do_wikicode_test(test_data, add_also)

if __name__ == "__main__":
    unittest.main()

