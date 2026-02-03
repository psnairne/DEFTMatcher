import hpotk
from hpotk import Ontology

from deft_matcher.matcher import Matcher
from deft_matcher.matchers.rag_hpo_matcher.candidate_retriever import (
    HpoCandidateRetriever,
)
from deft_matcher.ontology_class import OntologyClass
from deft_matcher.utils import get_oc


class HpoVectorSimilarityMatcher(Matcher):
    """
    Given an hpo_embeddings.npz file and a metadata.json file whose indexes agree with those of the embeddings,
    this matcher will retrieve candidate HPO terms based on a vector similarity search.
    """

    _ontology: Ontology
    _id_to_term: dict[str, OntologyClass]

    def __init__(
        self,
        embedded_hpo_path: str,
        embedding_metadata_path: str,
        embedding_model_path: str,
        similarity_threshold: float = 0.8,
    ) -> None:
        self.embedded_hpo_path = embedded_hpo_path
        self.embedding_metadata_path = embedding_metadata_path
        self.embedding_model_path = embedding_model_path
        self._hpo_candidate_retriever = HpoCandidateRetriever(
            embedded_hpo_path, embedding_metadata_path, embedding_model_path
        )
        # parameters for candidate retrieval
        self.similarity_threshold = similarity_threshold
        self._ontology = self._initialise_hpo()
        self._id_to_term = self._initialise_id_to_term()

    @staticmethod
    def _initialise_hpo() -> Ontology:
        store = hpotk.configure_ontology_store()
        return store.load_hpo(release="v2026-01-08")

    def _initialise_id_to_term(self) -> dict[str, OntologyClass]:
        return {term.identifier.value: get_oc(term) for term in self._ontology.terms}

    @property
    def name(self) -> str:
        return "HpoVectorSimilarityMatcher"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        candidate: str | None = self._hpo_candidate_retriever.get_most_similar(
            phrase=free_text,
            amount_to_search=500,
            similarity_threshold=self.similarity_threshold,
        )

        if candidate is None:
            return []
        else:
            hpo_term: OntologyClass = self._id_to_term[candidate]
            return [hpo_term]
