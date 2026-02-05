import os

import pytest
from deft_matcher.matchers.vector_similarity_matcher import HpoVectorSimilarityMatcher
from deft_matcher.ontology_class import OntologyClass


@pytest.fixture
def vector_similarity_matcher():
    embedded_hpo_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_embedded.npz"
    embedding_metadata_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_meta.json"
    embedding_model_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/sbert_model"
    return HpoVectorSimilarityMatcher(
        embedded_hpo_path=embedded_hpo_path,
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
