import os

import pytest
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_vec_similarity_matcher


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_vector_similarity_matcher():
    painful_leg_matches = hpo_vec_similarity_matcher().match("my leg hurts")

    assert painful_leg_matches == OntologyClass("HP:0012514", "Lower limb pain")
