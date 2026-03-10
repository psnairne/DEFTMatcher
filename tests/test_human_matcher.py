import pytest
from deft_matcher.matchers.human_matcher import HumanRetriever
from deft_matcher.matchers.human_matcher import MockInterface
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_syn_matcher


@pytest.fixture
def human_matcher():
    return HumanRetriever(MockInterface(), hpo_syn_matcher())


def test_human_matcher(human_matcher):
    osthma_matches = human_matcher.get_matches("Osthma")

    assert len(osthma_matches) == 1
    assert osthma_matches[0] == OntologyClass("HP:0002099", "Asthma")
