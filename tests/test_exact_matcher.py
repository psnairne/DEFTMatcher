import hpotk
import pytest
from hpotk import OntologyType

from deft_matcher.matchers.exact_matcher import ExactMatcher


@pytest.fixture
def exact_matcher_hpo():
    store = hpotk.configure_ontology_store()
    hpo = store.load_hpo(release="v2025-11-24")
    return ExactMatcher(hpo)


@pytest.fixture
def exact_matcher_mondo():
    store = hpotk.configure_ontology_store()
    mondo = store.load_ontology(
        ontology_type=OntologyType.MONDO,
        release="v2025-12-02",
        prefixes_of_interest={"MONDO"},
    )
    return ExactMatcher(mondo)


def test_exact_matcher_hpo_success(exact_matcher_hpo):
    asthma_matches = exact_matcher_hpo.get_matches("Asthma")

    assert len(asthma_matches) == 1
    assert asthma_matches[0] == "HP:0002099"


def test_exact_matcher_hpo_fail(exact_matcher_hpo):
    asthma_matches = exact_matcher_hpo.get_matches("Osthma")

    assert len(asthma_matches) == 0


def test_exact_matcher_mondo_success(exact_matcher_mondo):
    marfan_matches = exact_matcher_mondo.get_matches("marfan synDROME")

    assert len(marfan_matches) == 1
    assert marfan_matches[0] == "MONDO:0007947"


def test_exact_matcher_mondo_fail(exact_matcher_mondo):
    marfan_matches = exact_matcher_mondo.get_matches("morfan syndrome")

    assert len(marfan_matches) == 0
