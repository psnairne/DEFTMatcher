import os

import pytest
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_vec_similarity_retriever


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_vector_similarity_retriever():
    painful_leg_matches = hpo_vec_similarity_retriever(
        similarity_threshold=0, number_of_candidates=5
    ).get_matches("my leg hurts")

    assert len(painful_leg_matches) == 5
    assert painful_leg_matches[0] == OntologyClass("HP:0012514", "Lower limb pain")
