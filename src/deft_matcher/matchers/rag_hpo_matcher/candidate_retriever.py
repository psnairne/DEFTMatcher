import json
import re
from typing import List, Dict, Set

import faiss
import numpy as np
from faiss import IndexFlatIP
from numpy import ndarray

from sentence_transformers import SentenceTransformer


class HpoCandidateRetriever:
    """
    Sets up a FAISS index for a HPO vector embedding.

    Given a str phrase, this phrase can be embedded
    and then the FAISS index can be used for either a simple similarity search,
    or a hybrid similarity search.
    """

    embedded_hpo_path: str
    embedding_metadata_path: str
    embedding_model_path: str
    _emb_model: SentenceTransformer

    def __init__(
        self,
        embedded_hpo_path: str,
        embedding_metadata_path: str,
        embedding_model_path: str,
    ) -> None:
        self.embedded_hpo_path = embedded_hpo_path
        self.embedding_metadata_path = embedding_metadata_path
        self.embedding_model_path = embedding_model_path
        self._faiss_index = self._initialise_faiss_index()
        self._embedding_metadata = self._load_embedding_meta_data()
        self._emb_model = self._initialise_embeddings_model()

    def _initialise_faiss_index(self) -> IndexFlatIP:
        """
        Allows searches on the HPO embedding matrix.
        """
        emb_matrix: ndarray[np.float32] = np.load(self.embedded_hpo_path)["emb"].astype(
            np.float32
        )
        dim: int = emb_matrix.shape[1]
        faiss.normalize_L2(emb_matrix)
        faiss_index: IndexFlatIP = faiss.IndexFlatIP(dim)
        faiss_index.add(emb_matrix)  # type: ignore[arg-type]
        return faiss_index

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

    def _initialise_embeddings_model(self) -> SentenceTransformer:
        """
        Allows us to embed new phrases as 768 dimensional vectors.
        """
        return SentenceTransformer(self.embedding_model_path)

    def embed_phrase(self, phrase: str) -> ndarray[np.float32]:
        """
        Embed a phrase as a 768 dimensional vector.
        """
        vec: ndarray[np.float32] = self._emb_model.encode(phrase, convert_to_numpy=True)
        vec = vec.reshape(1, -1)
        faiss.normalize_L2(vec)
        return vec

    @staticmethod
    def _token_overlap(phrase1: str, phrase2: str) -> bool:
        tokens1: Set[str] = set(re.findall(r"\w+", phrase1.lower()))
        tokens2: Set[str] = set(re.findall(r"\w+", phrase2.lower()))
        return bool(tokens1 & tokens2)

    def get_candidates(
        self,
        phrase: str,
        amount_to_search: int,
        min_candidates: int,
        max_candidates: int,
        similarity_threshold: float,
        hybrid_search: bool,
    ) -> List[Dict[str, str]]:
        """
        Gets the best candidates based on cosine similarity score.
        If hybrid_search = True, then it also takes into account token overlap.
        """

        similarities: ndarray[float]
        indices: ndarray[int]

        query_vec: np.ndarray[np.float32] = self.embed_phrase(phrase)
        (similarities,), (indices,) = self._faiss_index.search(query_vec, amount_to_search)  # type: ignore[arg-type]

        seen_hpo_ids: Set[str] = set()
        candidates: List[Dict[str, str | float]] = []
        for similarity_score, idx in sorted(
            zip(similarities, indices), key=lambda x: x[0], reverse=True
        ):
            metadata: dict[str, str] = self._embedding_metadata[idx]
            hpo_id: str = metadata.get("hp_id")
            syn_or_label: str = metadata.get("info")

            if hpo_id in seen_hpo_ids:
                continue

            accept_candidate: bool

            if hybrid_search:
                accept_candidate = (
                    similarity_score >= similarity_threshold
                    or len(candidates) < min_candidates
                    or self._token_overlap(phrase, syn_or_label)
                )
            else:
                accept_candidate = (
                    similarity_score >= similarity_threshold
                    or len(candidates) < min_candidates
                )

            if accept_candidate:
                seen_hpo_ids.add(hpo_id)
                candidates.append(
                    {
                        "hpo_id": hpo_id,
                        "description": syn_or_label,
                        "similarity_score": float(similarity_score),
                    }
                )

            if len(candidates) >= max_candidates:
                break

        return candidates
