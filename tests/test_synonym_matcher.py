import pytest

from deft_matcher.matchers.synonym_matcher import SynonymMatcher
from deft_matcher.ontology_class import OntologyClass


@pytest.fixture
def synonym_matcher_hpo():
    return SynonymMatcher(
        "hp",
        "assets/ontology_obo_files/hp_v2026-02-16.obo",
        # phenotypic abnormality
        "HP:0000118",
    )


@pytest.fixture
def synonym_matcher_maxo():
    return SynonymMatcher(
        "maxo",
        "assets/ontology_obo_files/maxo_v2026-01-15.obo",
        # medical action
        "MAXO:0000001",
    )


def test_synonym_matcher_hpo_success(synonym_matcher_hpo):
    asd_matches = synonym_matcher_hpo.get_matches("ASD")

    assert len(asd_matches) == 2
    assert set(asd_matches) == {
        OntologyClass("HP:0000729", "Autistic behavior"),
        OntologyClass("HP:0001631", "Atrial septal defect"),
    }


def test_synonym_matcher_hpo_fail(synonym_matcher_hpo):
    asd_matches = synonym_matcher_hpo.get_matches("OSD")

    assert len(asd_matches) == 0


def test_synonym_matcher_maxo(synonym_matcher_maxo):
    mfs_matches = synonym_matcher_maxo.get_matches("aorta biopsy")
    assert len(mfs_matches) == 1
    assert set(mfs_matches) == {OntologyClass("MAXO:0000333", "biopsy of aorta")}
