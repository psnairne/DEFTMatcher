import json
from typing import List, Dict

from deft_matcher.matcher import Matcher
from deft_matcher.matchers.rag_hpo_matcher.candidate_retriever import (
    HpoCandidateRetriever,
)
from deft_matcher.matchers.rag_hpo_matcher.ollama_client import OllamaClient


class RagHpoMatcher(Matcher):
    """
    Uses a local LLM to try and match free text to HPO terms.
    The LLM is provided with a list of twenty or so possible candidate HPO terms as context.

    These candidate HPO terms are found via a vector similarity search.
    The vectorised HPO is found in hpo_embedded.npz.
    """

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
        self._hpo_candidate_retriever = HpoCandidateRetriever(
            embedded_hpo_path, embedding_metadata_path, embedding_model_path
        )
        # parameters for candidate retrieval
        self.amount_to_search = amount_to_search
        self.min_candidates = min_candidates
        self.max_candidates = max_candidates
        self.similarity_threshold = similarity_threshold
        self.hybrid_search = hybrid_search

    @property
    def name(self) -> str:
        return f"RagHpoMatcher({self.model_name})"

    def get_matches(self, free_text: str) -> list[str]:
        with open(
            "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/system_message.txt",
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

        return [self._client.query(system_message, user_input)]
