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

    model_name: str
    _client: OllamaClient
    embedded_hpo_path: str
    embedding_metadata_path: str
    embedding_model_path: str
    _client: OllamaClient
    _hpo_candidate_retriever: HpoCandidateRetriever

    def __init__(
        self,
        model_name: str,
        embedded_hpo_path: str,
        embedding_metadata_path: str,
        embedding_model_path: str,
    ) -> None:
        self.model_name = model_name
        self.embedded_hpo_path = embedded_hpo_path
        self.embedding_metadata_path = embedding_metadata_path
        self.embedding_model_path = embedding_model_path
        self._client = OllamaClient(model_name=self.model_name)
        self._hpo_candidate_retriever = HpoCandidateRetriever(
            embedded_hpo_path, embedding_metadata_path, embedding_model_path
        )

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

        candidates: List[Dict[str, str]] = (
            self._hpo_candidate_retriever.get_hybrid_candidates(
                phrase=free_text,
                amount_to_search=500,
                min_candidates=15,
                max_candidates=20,
                similarity_threshold=0.35,
            )
        )

        user_input: str = json.dumps({"phrase": free_text, "candidates": candidates})

        return [self._client.query(system_message, user_input)]
