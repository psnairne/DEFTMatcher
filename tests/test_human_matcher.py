import pytest

from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.human_matcher.user_interfaces.mock_interface import (
    MockInterface,
)
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_syn_retriever


@pytest.fixture
def human_matcher():
    return HumanMatcher(MockInterface(), hpo_syn_retriever())


def test_human_matcher(human_matcher):
    osthma_match = human_matcher.match("Osthma")

    assert osthma_match == OntologyClass("HP:0002099", "Asthma")
