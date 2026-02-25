import pytest

from deft_matcher.matchers.exact_matcher import ExactMatcher
from deft_matcher.ontology_class import OntologyClass


@pytest.fixture
def exact_matcher_hpo():
    return ExactMatcher(
        "hp",
        "assets/ontology_obo_files/hp_v2026-02-16.obo",
        # phenotypic abnormality
        "HP:0000118",
    )


@pytest.fixture
def exact_matcher_maxo():
    return ExactMatcher(
        "maxo",
        "assets/ontology_obo_files/maxo_v2026-01-15.obo",
        # medical action
        "MAXO:0000001",
    )


def test_exact_matcher_hpo_success(exact_matcher_hpo):
    asthma_matches = exact_matcher_hpo.get_matches("Asthma")

    assert len(asthma_matches) == 1
    assert asthma_matches[0] == OntologyClass("HP:0002099", "Asthma")


def test_exact_matcher_hpo_fail(exact_matcher_hpo):
    asthma_matches = exact_matcher_hpo.get_matches("Osthma")

    assert len(asthma_matches) == 0


def test_exact_matcher_maxo_success(exact_matcher_maxo):
    bht_matches = exact_matcher_maxo.get_matches("breath hydrOGEN test")

    assert len(bht_matches) == 1
    assert bht_matches[0] == OntologyClass("MAXO:0035096", "breath hydrogen test")


def test_exact_matcher_maxo_fail(exact_matcher_maxo):
    bht_matches = exact_matcher_maxo.get_matches("broth hydrogen test")

    assert len(bht_matches) == 0
