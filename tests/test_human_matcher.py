import hpotk
import pytest
from hpotk import OntologyStore, Ontology

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
def store() -> OntologyStore:
    return hpotk.configure_ontology_store()


@pytest.fixture
def hpo(store) -> Ontology:
    return store.load_hpo(release="v2025-11-24")


@pytest.fixture
def hpo_syn_matcher(hpo) -> SynonymMatcher:
    return SynonymMatcher(ontology=hpo)


@pytest.fixture
def human_matcher(hpo_syn_matcher):
    interface: UserInterface = MockInterface()
    candidate_retriever: Matcher = hpo_syn_matcher
    return HumanMatcher(interface, candidate_retriever)


def test_human_matcher(human_matcher):
    osthma_matches = human_matcher.get_matches("Osthma")

    assert len(osthma_matches) == 1
    assert osthma_matches[0] == OntologyClass("HP:0002099", "Asthma")
