"""
Test hyphenation functions
"""

from kamusi import get_hyphenations


def test_no_pattern():
    """
    Test case for no hyphenation
    """
    pattern = "{{audio|de|De-Laugen.ogg|Audio}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_single_pattern():
    """
    Test case for one hyphenation
    """
    pattern = "{{hyph|de|Ers|ter Golf|krieg}}"
    hyph = ["Ers|ter Golf|krieg"]
    assert list(get_hyphenations(pattern)) == hyph


def test_double_pattern_in_one():
    """
    Test case for two hyphenations in one template
    """
    pattern = "{{hyph|de|apo|s|t|ro|phie|ren||apo|stro|phie|ren}}"
    hyph = ["apo|s|t|ro|phie|ren", "apo|stro|phie|ren"]
    assert list(get_hyphenations(pattern)) == hyph


def test_double_pattern_in_two():
    """
    Test case for two hyphenations in two templates
    """
    pattern = (
        "{{hyph|de|apo|s|t|ro|phie|ren}}, {{hyph|de|apo|stro|phie|ren|nocaption=1}}"
    )
    hyph = ["apo|s|t|ro|phie|ren", "apo|stro|phie|ren"]
    assert list(get_hyphenations(pattern)) == hyph
