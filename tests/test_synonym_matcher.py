import hpotk
import pytest
from hpotk import SynonymType, SynonymCategory

from deft_matcher.matchers.synonym_matcher import SynonymMatcher


@pytest.fixture
def hpo():
    store = hpotk.configure_ontology_store()
    return store.load_hpo(release="v2025-11-24")


@pytest.fixture
def synonym_matcher_hpo(hpo):
    return SynonymMatcher(hpo)


def test_synonym_matcher_hpo_success(synonym_matcher_hpo):
    asd_matches = synonym_matcher_hpo.get_matches("ASD")

    assert len(asd_matches) == 2
    assert set(asd_matches) == {
        "HP:0000729",  # HP:0000729 Autistic behaviour
        "HP:0001631",  # HP:0001631 Atrial Septal Defect
    }


def test_synonym_matcher_hpo_fail(synonym_matcher_hpo):
    asd_matches = synonym_matcher_hpo.get_matches("OSD")

    assert len(asd_matches) == 0


def test_synonym_matcher_restrict_by_category(hpo):
    uk_synonym_matcher = SynonymMatcher(hpo, synonym_types=[SynonymType.UK_SPELLING])

    asd_matches = uk_synonym_matcher.get_matches("ASD")

    assert len(asd_matches) == 0


def test_synonym_matcher_restrict_by_type(hpo):
    broad_synonym_matcher = SynonymMatcher(
        hpo, synonym_categories=[SynonymCategory.BROAD]
    )

    asd_matches = broad_synonym_matcher.get_matches("ASD")

    assert len(asd_matches) == 0


def test_synonym_matcher_restrict_by_category_and_type(hpo):
    abbreviation_exact_synonym_matcher = SynonymMatcher(
        hpo,
        synonym_types=[SynonymType.ABBREVIATION],
        synonym_categories=[SynonymCategory.EXACT],
    )
    asd_matches = abbreviation_exact_synonym_matcher.get_matches("ASD")

    assert len(asd_matches) == 2
    assert set(asd_matches) == {
        "HP:0000729",  # HP:0000729 Autistic behaviour
        "HP:0001631",  # HP:0001631 Atrial Septal Defect
    }
