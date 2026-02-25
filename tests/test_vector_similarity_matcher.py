import os

import pytest

from deft_matcher.matchers.vector_similarity_matcher.vector_similarity_matcher import (
    VectorSimilarityMatcher,
)
from deft_matcher.ontology_class import OntologyClass


@pytest.fixture
def vector_similarity_matcher():
    hpo_obo_path = "assets/ontology_obo_files/hp_v2026-02-16.obo"
    embedded_hpo_path = "assets/vector_similarity_matcher_data/data/hpo_embedded.npz"
    embedding_metadata_path = "assets/vector_similarity_matcher_data/data/hpo_meta.json"
    embedding_model_path = "assets/vector_similarity_matcher_data/sbert_model"
    return VectorSimilarityMatcher(
        ontology_prefix="hp",
        ontology_obo_path=hpo_obo_path,
        root_term="HP:0000001",
        embedding_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
        similarity_threshold=0.65,
        max_candidates=1,
    )


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_vector_similarity_matcher(vector_similarity_matcher):
    painful_leg_matches = vector_similarity_matcher.get_matches("my leg hurts")

    assert len(painful_leg_matches) == 1
    assert painful_leg_matches[0] == OntologyClass("HP:0012514", "Lower limb pain")
