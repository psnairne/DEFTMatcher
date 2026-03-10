import pytest

from deft_matcher.matchers.constant_matcher import ConstantRetriever
from deft_matcher.ontology_class import OntologyClass


@pytest.fixture
def oc() -> OntologyClass:
    return OntologyClass("MONDO:0007947", "Marfan syndrome")


@pytest.fixture
def constant_matcher(oc: OntologyClass) -> ConstantRetriever:
    return ConstantRetriever(oc)


def test_constant_matcher(constant_matcher: ConstantRetriever, oc: OntologyClass):
    match = constant_matcher.get_matches("Asthma")

    assert len(match) == 1
    assert match[0] == oc
