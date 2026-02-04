import pytest

from deft_matcher.matchers.human_matcher import HumanMatcher
from deft_matcher.matcher import Matcher
from deft_matcher.matchers.vector_similarity_matcher import HpoVectorSimilarityMatcher
from deft_matcher.ontology_class import OntologyClass
from deft_matcher.matchers.human_matcher.user_interfaces import MockInterface
from deft_matcher.matchers.human_matcher.user_interfaces import UserInterface


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


@pytest.fixture
def human_matcher(vector_similarity_matcher):
    interface: UserInterface = MockInterface()
    candidate_retriever: Matcher = vector_similarity_matcher
    return HumanMatcher(interface, candidate_retriever)


def test_human_matcher(human_matcher):
    osthma_matches = human_matcher.get_matches("Osthma")

    assert len(osthma_matches) == 1
    assert osthma_matches[0] == OntologyClass("HP:0002099", "Asthma")
