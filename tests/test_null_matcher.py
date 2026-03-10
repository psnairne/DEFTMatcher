import pytest

from deft_matcher.matchers.null_matcher import NullMatcher
from deft_matcher.ontology_class import OntologyClass


@pytest.fixture
def null_matcher() -> NullMatcher:
    return NullMatcher()


def test_null_matcher(null_matcher: NullMatcher):
    null_match = null_matcher.match("Asthma")

    assert null_match == OntologyClass("", "")
