"""
Test hyphenation functions
"""

from kamusi import Hyphenation, get_hyphenations


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
    hyph = [["Ers", "ter Golf", "krieg"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_double_pattern_in_one():
    """
    Test case for two hyphenations in one template
    """
    pattern = "{{hyph|de|apo|s|t|ro|phie|ren||apo|stro|phie|ren}}"
    hyph = [["apo", "s", "t", "ro", "phie", "ren"], ["apo", "stro", "phie", "ren"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_double_pattern_in_two():
    """
    Test case for two hyphenations in two templates
    """
    pattern = (
        "{{hyph|de|apo|s|t|ro|phie|ren}}, {{hyph|de|apo|stro|phie|ren|nocaption=1}}"
    )
    hyph = [["apo", "s", "t", "ro", "phie", "ren"], ["apo", "stro", "phie", "ren"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_no_pattern_pl():
    """
    Test case for a Polish template without hyphenation
    """
    pattern = "{{pl-p|a=LL-Q809 (pol)-Olaf-pożywić.wav}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_single_pattern_pl():
    """
    Test case for a Polish template with one hyphenation
    """
    pattern = "{{pl-p|de'ko.rum|h=de.co.rum}}"
    hyph = [["de", "co", "rum"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_double_pattern_pl():
    """
    Test case for a Polish template with two hyphenations
    """
    pattern = "{{pl-p|'prze.r-znąć|'przer.znąć|h1=prze.rznąć|h2=przer.znąć}}"
    hyph = [["prze", "rznąć"], ["przer", "znąć"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_hyph_is_valid():
    """
    Test simple cases of is_valid()
    """
    assert Hyphenation("abbrechen", ["ab", "bre", "chen"]).is_valid()
    assert not Hyphenation("wrong", ["ab", "bre", "chen"]).is_valid()
