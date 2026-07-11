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
    def run_test(self, case: str, action: Callable[[WiktionaryPage], None], lang="en"):
        test_data = self.get_test_data("also", case)

        def do_operation(test_data):
            page = kamusi.WiktionaryPage.with_language_edition(
                title=test_data.page_title,
                site_lang=lang,
                from_text=test_data.before
            )
            action(page)
            return page

        self.do_wikicode_test(test_data, do_operation)

    def test_en_add(self):
        def add_also(page):
            page.also = ["Hima"]

        self.run_test("en_add_new", add_also)

    def test_en_modify(self):
        def modify_also(page):
            page.also = ["Brother", "broþer"]

        self.run_test("en_modify", modify_also)

    def test_en_remove(self):
        def remove_also(page):
            del page.also

        self.run_test("en_remove", remove_also)

if __name__ == "__main__":
    unittest.main()

