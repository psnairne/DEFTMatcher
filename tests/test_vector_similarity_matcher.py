import os

import pytest
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import vector_similarity_matcher


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_vector_similarity_matcher():
    painful_leg_matches = vector_similarity_matcher().get_matches("my leg hurts")

    assert len(painful_leg_matches) == 1
    assert painful_leg_matches[0] == OntologyClass("HP:0012514", "Lower limb pain")
