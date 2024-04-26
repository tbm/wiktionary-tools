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


def test_empty_pattern_es():
    """
    Test case for a Spanish template without hyphenation
    """
    pattern = "{{es-pr}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_no_pattern_es():
    """
    Test case for a Spanish template without hyphenation
    """
    pattern = "{{es-pr|+,shóchil}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_plus_pattern_es():
    """
    Test case for a Spanish template with + hyphenation
    """
    pattern = "{{es-pr|adisoniano<hyph:+>}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_single_pattern_es():
    """
    Test case for a Spanish template with one hyphenation
    """
    pattern = "{{es-pr|Tlajiaco<hyph:Tla.xia.co>}}"
    hyph = [["Tla", "xia", "co"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_double_pattern_es():
    """
    Test case for a Spanish template with two hyphenations
    """
    pattern = "{{es-pr|+<hyph:de.sam.pa.rar, des.am.pa.rar>}}"
    hyph = [["de", "sam", "pa", "rar"], ["des", "am", "pa", "rar"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_empty_pattern_it():
    """
    Test case for an Italian template without hyphenation
    """
    pattern = "{{it-pr}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_no_pattern_it():
    """
    Test case for an Italian template without hyphenation
    """
    pattern = "{{it-pr|òcimo}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_minus_pattern_it():
    """
    Test case for an Italian template with - hyphenation
    """
    pattern = "{{it-pr|pàssword<hyph:->}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_single_pattern_it():
    """
    Test case for an Italian template with one hyphenation
    """
    pattern = "{{it-pr|Kalèd<r:DiPI><hyph:Kha.led>}}"
    hyph = [["Kha", "led"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_double_pattern_it():
    """
    Test case for an Italian template with two hyphenations
    """
    pattern = "{{it-pr|macète,macéte<hyph:ma.chè.te,ma.ché.te>}}"
    hyph = [["ma", "chè", "te"], ["ma", "ché", "te"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_empty_pattern_fi():
    """
    Test case for a Finnish template without hyphenation
    """
    pattern = "{{fi-p}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_no_pattern_fi():
    """
    Test case for a Finnish template without hyphenation
    """
    pattern = "{{fi-p|kurkku-tauti}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_single_pattern_fi():
    """
    Test case for a Finnish template with one hyphenation
    """
    pattern = "{{fi-p|keres|h=Ce.res}}"
    hyph = [["Ce", "res"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_single_pattern_fi_long():
    """
    Test case for a Finnish template with one hyphenation
    """
    pattern = "{{fi-pronunciation|tsodiakki|h=zo.di.ak.ki|r=ɑkːi}}"
    hyph = [["zo", "di", "ak", "ki"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_double_pattern_fi():
    """
    Test case for a Finnish template with two hyphenations
    """
    pattern = "{{fi-p|gurka|gurkha|r1=urka|r2=urkha|h1=gur.kha|h2=gurk.ha}}"
    hyph = [["gur", "kha"], ["gurk", "ha"]]
    assert list(get_hyphenations(pattern)) == hyph


def test_no_pattern_pl():
    """
    Test case for a Polish template without hyphenation
    """
    pattern = "{{pl-p|a=LL-Q809 (pol)-Olaf-pożywić.wav}}"
    hyph = []
    assert list(get_hyphenations(pattern)) == hyph


def test_none_pattern_pl():
    """
    Test case for a Polish template without hyphenation
    """
    pattern = "{{pl-p|atmosfera|h=-|r=-}}"
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
    assert Hyphenation.create("acel·lular", ["a", "cel", "lu", "lar"], "ca").is_valid()


def test_hyph_is_valid_de_ck_kk():
    """
    Test is_valid() for German for the ck -> kk change
    """
    assert Hyphenation.create("Glocke", ["Glok", "ke"], "de").is_valid()
    assert Hyphenation.create("Hecke", ["Hek", "ke"], "de").is_valid()
    assert Hyphenation.create("Muckefuck", ["Muk", "ke", "fuck"], "de").is_valid()


def test_hyph_is_valid_de_exceptions():
    """
    Test is_valid() for special cases in German
    """
    assert Hyphenation.create("dämmrig", ["däm", "me", "rig"], "de").is_valid()
    assert Hyphenation.create("Brennessel", ["Brenn", "nes", "sel"], "de").is_valid()
    assert Hyphenation.create(
        "justiziabel", ["ju", "sti", "tia", "bel"], "de"
    ).is_valid()


def test_hyph_is_valid_hu():
    """
    Test is_valid() for Hungarian
    """
    assert Hyphenation.create("üccsi", ["ücs", "csi"], "hu").is_valid()
    assert Hyphenation.create("süllyed", ["süly", "lyed"], "hu").is_valid()
    assert Hyphenation.create("vinnyog", ["viny", "nyog"], "hu").is_valid()
    assert Hyphenation.create("ősszel", ["ősz", "szel"], "hu").is_valid()
    assert Hyphenation.create("szattyán", ["szaty", "tyán"], "hu").is_valid()


def test_hyph_is_valid_it():
    """
    Test is_valid() for Italian
    """
    assert Hyphenation.create(
        "adenoidea", ["a", "de", "noi", "dè", "a"], "it"
    ).is_valid()
    assert Hyphenation.create("biroldo", ["bi", "ról", "do"], "it").is_valid()


def test_hyph_is_valid_nl():
    """
    Test is_valid() for Dutch
    """
    assert Hyphenation.create("Caïro", ["Ca", "i", "ro"], "nl").is_valid()
    assert Hyphenation.create("Chassébuurt", ["Chas", "se", "buurt"], "nl").is_valid()
    assert Hyphenation.create("Daniël", ["Da", "ni", "el"], "nl").is_valid()


def test_hyph_is_valid_yi():
    """
    Test is_valid() for Yiddish
    """
    assert Hyphenation.create("קרעבס־עסער", ["קרעבס", "ע", "סער"], "yi").is_valid()
