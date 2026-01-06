import json
import re
from typing import List, Dict, cast, Tuple

import faiss
import numpy as np
from faiss import IndexFlatIP
from numpy._typing import NDArray

from deft_matcher.matcher import Matcher
from deft_matcher.matchers.rag_hpo_matcher.ollama_client import OllamaClient

from sentence_transformers import SentenceTransformer


class RagHpoMatcher(Matcher):
    """
    Uses a local LLM to try and match free text to HPO terms.
    The LLM is provided with a list of twenty possible candidate HPO terms as context.

    These candidate HPO terms are found via a vector similarity search.
    The vectorised HPO is found in hpo_embedded.npz.
    """

    model_name: str
    _client: OllamaClient
    embedded_hpo_path: str
    embedding_metadata_path: str
    embedding_model_path: str
    _emb_model: SentenceTransformer

    def __init__(
        self,
        model_name: str,
        embedded_hpo_path: str,
        embedding_metadata_path: str,
        embedding_model_path: str,
    ) -> None:
        self.model_name = model_name
        self._client = OllamaClient(model_name=self.model_name)
        self.embedded_hpo_path = embedded_hpo_path
        self.embedding_metadata_path = embedding_metadata_path
        self.embedding_model_path = embedding_model_path
        self._emb_model = self._initialise_embeddings_model()
        self._faiss_index = self._initialise_faiss_index()
        self._embedding_metadata = self._load_embedding_meta_data()

    @property
    def name(self) -> str:
        return f"RagHpoMatcher({self.model_name})"

    def _initialise_embeddings_model(self) -> SentenceTransformer:
        return SentenceTransformer(self.embedding_model_path)

    def _load_embedding_meta_data(self) -> List[Dict[str, str]]:
        """
        Output is a list of dictionaries of the form
        {
            'hp_id': HPO ID,
            'info': synonym or label
        }

        The order of the list, corresponds to the order of the embedding matrix,
        and to the indices returned by a search on the FAISS index.
        """
        with open(self.embedding_metadata_path, "r", encoding="utf-8") as f:
            entries = json.load(f).get("entries", [])
        return [{k: v for k, v in e.items() if k != "direction"} for e in entries]

    def _initialise_faiss_index(self) -> IndexFlatIP:
        emb_matrix: NDArray[np.float32] = np.load(self.embedded_hpo_path)["emb"].astype(
            np.float32
        )
        dim: int = emb_matrix.shape[1]
        faiss.normalize_L2(emb_matrix)
        faiss_index: IndexFlatIP = faiss.IndexFlatIP(dim)
        faiss_index.add(emb_matrix)  # type: ignore[arg-type]
        return faiss_index

    @staticmethod
    def _embed_phrase(phrase: str, model: SentenceTransformer) -> NDArray[np.float32]:
        vec: NDArray[np.float32] = model.encode(phrase, convert_to_numpy=True)
        vec = vec.reshape(1, -1)
        faiss.normalize_L2(vec)
        return vec

    def _get_candidates(
        self,
        phrase: str,
        amount_to_search: int,
        min_unique: int,
        max_unique: int,
        similarity_threshold: float,
    ) -> List[Dict[str, str]]:

        query_vec = self._embed_phrase(phrase, self._emb_model)
        (similarities,), (indices,) = self._faiss_index.search(query_vec, amount_to_search)  # type: ignore[arg-type]

        seen_hpo_ids = set()
        candidates = []
        for similarity_score, idx in sorted(
            zip(similarities, indices), key=lambda x: x[0], reverse=True
        ):
            if len(candidates) >= max_unique:
                break

            metadata = self._embedding_metadata[idx]
            hpo_id = metadata.get("hp_id")
            syn_or_label = metadata.get("info")

            if not syn_or_label:
                raise Exception("syn_or_label was empty")

            if not hpo_id:
                raise Exception("hpo_id was empty")

            if hpo_id in seen_hpo_ids:
                continue

            clean_tokens = set(re.findall(r"\w+", phrase.lower()))
            token_overlap = bool(
                clean_tokens & set(re.findall(r"\w+", syn_or_label.lower()))
            )

            # accept if token overlap, or above similarity threshold, or to reach min_unique
            if (
                token_overlap
                or similarity_score >= similarity_threshold
                or len(candidates) < min_unique
            ):
                seen_hpo_ids.add(hpo_id)
                candidates.append(
                    {
                        "hpo_id": hpo_id,
                        "description": syn_or_label,
                        "similarity_score": float(similarity_score),
                    }
                )

        return candidates

    def get_matches(self, free_text: str) -> list[str]:

        candidates: List[Dict[str, str]] = self._get_candidates(
            phrase=free_text,
            amount_to_search=500,
            min_unique=15,
            max_unique=20,
            similarity_threshold=0.35,
        )

        print(candidates)

        user_input: str = json.dumps({"phrase": free_text, "candidates": candidates})

        with open(
            "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/system_message.txt",
            "r",
            encoding="utf-8",
        ) as f:
            system_message = f.read()

        resp: str = self._client.query(user_input, system_message)
        return [resp]
