import os

import pytest
from deft_matcher.matchers.deprecated.rag_hpo_matcher import RagHpoMatcher
from deft_matcher.ontology_class import OntologyClass


@pytest.fixture
def rag_hpo_matcher():
    model_name = "llama3.2"
    embedded_hpo_path = (
        "/deft_matcher/matchers/vector_similarity_matcher/data/hpo_embedded.npz"
    )
    embedding_metadata_path = (
        "/deft_matcher/matchers/vector_similarity_matcher/data/hpo_meta.json"
    )
    embedding_model_path = (
        "/deft_matcher/matchers/vector_similarity_matcher/sbert_model"
    )
    return RagHpoMatcher(
        model_name=model_name,
        embedded_hpo_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
    )


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_rag_hpo_matcher(rag_hpo_matcher):
    painful_leg_matches = rag_hpo_matcher.get_matches("my leg hurts")

    assert len(painful_leg_matches) == 1
    assert painful_leg_matches[0] == OntologyClass("HP:0012514", "Lower limb pain")
