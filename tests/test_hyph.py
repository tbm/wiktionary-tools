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


def test_hyph_eq():
    """
    Test whether Hyphenation() instances are equal
    """
    hyph1 = Hyphenation("abbrechen", ["ab", "bre", "chen"])
    hyph2 = Hyphenation("vorleisten", ["vor", "leis", "ten"])
    hyph3 = Hyphenation("vorleisten", ["vor", "lei", "sten"])
    hyph4 = Hyphenation("vorleisten", ["vor", "lei", "sten"])
    assert hyph1 == hyph1  # pylint: disable=comparison-with-itself
    assert hyph1 != hyph2
    assert hyph2 != hyph3
    assert hyph3 == hyph4


def test_hyph_is_valid():
    """
    Test simple cases of is_valid()
    """
    assert Hyphenation("abbrechen", ["ab", "bre", "chen"]).is_valid()
    assert not Hyphenation("wrong", ["ab", "bre", "chen"]).is_valid()


def test_hyph_is_valid_permissive():
    """
    Test some patterns with unclear behaviour that we accept for now
    """
    assert Hyphenation("Saint-Pierre", ["Saint", "Pierre"])
    assert Hyphenation("arménien ancien", ["ar", "mé", "nien", "an", "cien"])

def test_hyph_is_valid_ca():
    """
    Test is_valid() for Catalan
    """
    assert Hyphenation("acel·lular", ["a", "cel", "lu", "lar"], "ca").is_valid()

def test_hyph_is_valid_de():
    """
    Test is_valid() for German
    """
    assert Hyphenation("Glocke", ["Glok", "ke"], "de").is_valid()
    assert Hyphenation("Hecke", ["Hek", "ke"], "de").is_valid()
    assert Hyphenation("Muckefuck", ["Muk", "ke", "fuck"], "de").is_valid()

def test_hyph_is_valid_yi():
    """
    Test is_valid() for Yiddish
    """
    assert Hyphenation("קרעבס־עסער", ["קרעבס", "ע", "סער"], "yi").is_valid()
