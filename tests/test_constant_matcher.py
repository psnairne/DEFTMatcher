import pytest

from deft_matcher.matchers.constant_matcher import ConstantMatcher
from deft_matcher.ontology_class import OntologyClass


@pytest.fixture
def oc() -> OntologyClass:
    return OntologyClass("MONDO:0007947", "Marfan syndrome")


@pytest.fixture
def constant_matcher(oc: OntologyClass) -> ConstantMatcher:
    return ConstantMatcher(oc)


def test_constant_matcher(constant_matcher: ConstantMatcher, oc: OntologyClass):
    match = constant_matcher.match("Asthma")

    assert match == oc
