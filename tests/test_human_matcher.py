import pytest

from deft_matcher.matcher import Matcher
from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.human_matcher.user_interfaces.mock_interface import (
    MockInterface,
)
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)
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
def human_matcher(synonym_matcher_hpo):
    interface: UserInterface = MockInterface()
    candidate_retriever: Matcher = synonym_matcher_hpo
    return HumanMatcher(interface, candidate_retriever)


def test_human_matcher(human_matcher):
    osthma_matches = human_matcher.get_matches("Osthma")

    assert len(osthma_matches) == 1
    assert osthma_matches[0] == OntologyClass("HP:0002099", "Asthma")
