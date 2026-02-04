import pytest

from deft_matcher.matchers.constant_matcher import ConstantMatcher
from deft_matcher.ontology_class import OntologyClass


@pytest.fixture
def constant_matcher_null():
    oc = OntologyClass("", "")
    return ConstantMatcher(oc)


def test_constant_matcher(constant_matcher_null):
    null_match = constant_matcher_null.get_matches("Asthma")

    assert len(null_match) == 1
    assert null_match[0] == OntologyClass("", "")
