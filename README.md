
This repository contains a number of Python scripts and modules for Wiktionary (mostly English Wiktionary).

## Scripts

* `checks` -- various QA checks
* `download` -- downloads all lemmas of a given language
* `edit` -- tools to edit pages (add Wikipedia link, thumbnail and category)
* `fixes` -- tools to apply various fixes

## Modules

* `kamusi` -- a Python module to interact with English Wiktionary
* `isofyi` --  Python module for the Swedish-Yiddish dictionary published by the Swedish Institute or Language and Folklore (ISOF)

## Set up environment

You can set up your environment like this:

    python3 -m venv .venv --prompt "wikt"
    source .venv/bin/activate
    pip install -e .

## License

[GNU General Public License (GPL)](https://www.gnu.org/licenses/gpl-3.0.en.html), version 3 or above

Some test cases are taken from Wiktionary; they are distributed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

