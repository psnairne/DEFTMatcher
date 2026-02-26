from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_exact_matcher, maxo_exact_matcher


def test_exact_matcher_hpo_success():
    asthma_matches = hpo_exact_matcher().get_matches("Asthma")

    assert len(asthma_matches) == 1
    assert asthma_matches[0] == OntologyClass("HP:0002099", "Asthma")


def test_exact_matcher_hpo_fail():
    asthma_matches = hpo_exact_matcher().get_matches("Osthma")

    assert len(asthma_matches) == 0


def test_exact_matcher_maxo_success():
    bht_matches = maxo_exact_matcher().get_matches("breath hydrOGEN test")

    assert len(bht_matches) == 1
    assert bht_matches[0] == OntologyClass("MAXO:0035096", "breath hydrogen test")


def test_exact_matcher_maxo_fail():
    bht_matches = maxo_exact_matcher().get_matches("broth hydrogen test")

    assert len(bht_matches) == 0
