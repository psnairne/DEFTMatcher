import json
from typing import List, Dict

import hpotk
from hpotk import Ontology

from deft_matcher.matcher import Matcher
from deft_matcher.matchers.vector_similarity_matcher.candidate_retriever import (
    CandidateRetriever,
)
from deft_matcher.matchers.deprecated.ollama_client import OllamaClient
from deft_matcher.ontology_class import OntologyClass


class RagHpoMatcher(Matcher):
    """
    Uses a local LLM to try and match free text to HPO terms.
    The LLM is provided with a list of twenty or so possible candidate HPO terms as context.

    These candidate HPO terms are found via a vector similarity search.
    The vectorised HPO is found in hpo_embedded.npz.
    """

    _hpo: Ontology
    _id_to_term: dict[str, OntologyClass]

    def __init__(
        self,
        model_name: str,
        embedded_hpo_path: str,
        embedding_metadata_path: str,
        embedding_model_path: str,
        amount_to_search: int = 500,
        min_candidates: int = 15,
        max_candidates: int = 20,
        similarity_threshold: float = 0.35,
        hybrid_search: bool = True,
    ) -> None:
        self.model_name = model_name
        self.embedded_hpo_path = embedded_hpo_path
        self.embedding_metadata_path = embedding_metadata_path
        self.embedding_model_path = embedding_model_path
        self._client = OllamaClient(model_name=self.model_name)
        self._hpo_candidate_retriever = CandidateRetriever(
            embedded_hpo_path, embedding_metadata_path, embedding_model_path
        )
        # parameters for candidate retrieval
        self.amount_to_search = amount_to_search
        self.min_candidates = min_candidates
        self.max_candidates = max_candidates
        self.similarity_threshold = similarity_threshold
        self.hybrid_search = hybrid_search
        self._hpo = self._initialise_hpo()
        self._id_to_term = self._initialise_id_to_term()

    @staticmethod
    def _initialise_hpo() -> Ontology:
        store = hpotk.configure_ontology_store()
        return store.load_hpo(release="v2026-01-08")

    def _initialise_id_to_term(self) -> dict[str, OntologyClass]:
        return {
            term.identifier.value: OntologyClass.from_minimal_term(term)
            for term in self._hpo.terms
        }

    @property
    def name(self) -> str:
        return f"RagHpoMatcher({self.model_name})"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        with open(
            "/deft_matcher/matchers/deprecated/system_message.txt",
            "r",
            encoding="utf-8",
        ) as f:
            system_message: str = f.read()

        candidates: List[Dict[str, str]] = self._hpo_candidate_retriever.get_candidates(
            phrase=free_text,
            amount_to_search=self.amount_to_search,
            min_candidates=self.min_candidates,
            max_candidates=self.max_candidates,
            similarity_threshold=self.similarity_threshold,
            hybrid_search=self.hybrid_search,
        )

        user_input: str = json.dumps({"phrase": free_text, "candidates": candidates})

        llm_response: str = self._client.query(system_message, user_input)
        hpo_term: OntologyClass = self._id_to_term[llm_response]

        return [hpo_term]
