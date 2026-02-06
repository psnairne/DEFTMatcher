import hpotk
from hpotk import Ontology

from deft_matcher.matcher import Matcher
from deft_matcher.matchers.rag_hpo_matcher.candidate_retriever import (
    HpoCandidateRetriever,
)
from deft_matcher.ontology_class import OntologyClass


class HpoVectorSimilarityMatcher(Matcher):
    """
    Given an hpo_embeddings.npz file and a metadata.json file whose indexes agree with those of the embeddings,
    this matcher will retrieve candidate HPO terms based on a vector similarity search.

    Note: the version of the embedded HPO MUST agree with the version of HPO taken from HPO-toolkit.
    """

    _ontology: Ontology
    _id_to_term: dict[str, OntologyClass]

    def __init__(
        self,
        embedded_hpo_path: str,
        embedding_metadata_path: str,
        embedding_model_path: str,
        similarity_threshold: float = 0.8,
        max_candidates: int = 1,
    ) -> None:
        self.embedded_hpo_path = embedded_hpo_path
        self.embedding_metadata_path = embedding_metadata_path
        self.embedding_model_path = embedding_model_path
        self._hpo_candidate_retriever = HpoCandidateRetriever(
            embedded_hpo_path, embedding_metadata_path, embedding_model_path
        )
        # parameters for candidate retrieval
        self.similarity_threshold = similarity_threshold
        self.max_candidates = max_candidates
        self._ontology = self._initialise_hpo()
        self._id_to_term = self._initialise_id_to_term()

    @staticmethod
    def _initialise_hpo() -> Ontology:
        store = hpotk.configure_ontology_store()
        return store.load_hpo(release="v2025-11-24")

    def _initialise_id_to_term(self) -> dict[str, OntologyClass]:
        return {
            term.identifier.value: OntologyClass.from_minimal_term(term)
            for term in self._ontology.terms
        }

    @property
    def name(self) -> str:
        return "HpoVectorSimilarityMatcher"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        candidates: list[str] = self._hpo_candidate_retriever.get_most_similar(
            phrase=free_text,
            amount_to_search=500,
            similarity_threshold=self.similarity_threshold,
            max_candidates=self.max_candidates,
        )

        return [self._id_to_term[candidate] for candidate in candidates]
