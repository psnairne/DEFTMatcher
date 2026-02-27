import json

import faiss
import numpy as np
from faiss import IndexFlatIP
from numpy import ndarray

from sentence_transformers import SentenceTransformer


class CandidateRetriever:
    """
    Sets up a FAISS index for an ontology vector embedding.

    Given a str phrase, this phrase can be embedded
    and then the FAISS index can be used for either a simple similarity search,
    or a hybrid similarity search.
    """

    embedding_path: str
    embedding_metadata_path: str
    embedding_model_path: str
    _embedding_metadata = list[str]
    _emb_model: SentenceTransformer

    def __init__(
        self,
        embedding_path: str,
        embedding_metadata_path: str,
        embedding_model_path: str,
    ) -> None:
        self.embedding_path = embedding_path
        self.embedding_metadata_path = embedding_metadata_path
        self.embedding_model_path = embedding_model_path
        self._faiss_index = self._initialise_faiss_index()
        self._embedding_metadata = self._load_embedding_meta_data()
        self._emb_model = self._initialise_embeddings_model()

    def _initialise_faiss_index(self) -> IndexFlatIP:
        """
        Allows searches on the vector embedding matrix.
        """
        emb_matrix: ndarray[np.float32] = np.load(self.embedding_path)["emb"].astype(
            np.float32
        )
        dim: int = emb_matrix.shape[1]
        faiss.normalize_L2(emb_matrix)
        faiss_index: IndexFlatIP = faiss.IndexFlatIP(dim)
        faiss_index.add(emb_matrix)  # type: ignore[arg-type]
        return faiss_index

    def _load_embedding_meta_data(self) -> list[str]:
        """
        Output is a list of HPO IDs corresponding to the vectors in the embedding matrix.

        The order of the list, corresponds to the order of the embedding matrix,
        and to the indices returned by a search on the FAISS index.
        """
        with open(self.embedding_metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # Extract only the embedded_text_id.value field
        return [
            metadata_element["embedded_text_id"]["value"]
            for metadata_element in metadata
        ]

    def _initialise_embeddings_model(self) -> SentenceTransformer:
        """
        Allows us to embed new phrases as 768 dimensional vectors.
        """
        return SentenceTransformer(self.embedding_model_path)

    def embed_phrase(self, phrase: str) -> ndarray[np.float32]:
        """
        Embed a phrase as a 768 dimensional vector.
        """
        vec: ndarray[np.float32] = self._emb_model.encode(
            phrase, convert_to_numpy=True, show_progress_bar=False
        )
        vec = vec.reshape(1, -1)
        faiss.normalize_L2(vec)
        return vec

    def get_most_similar(
        self, phrase: str, similarity_threshold: float, max_candidates: int
    ) -> list[str]:
        """
        Retrieves the best candidates based on cosine similarity score.
        """

        similarities: ndarray[float]
        indices: ndarray[int]

        query_vec: np.ndarray[np.float32] = self.embed_phrase(phrase)
        (similarities,), (indices,) = self._faiss_index.search(query_vec, 500)  # type: ignore[arg-type]

        seen_ids: set[str] = set()
        candidates: list[str] = []

        ranked_search_results = sorted(
            zip(similarities, indices), key=lambda pair: pair[0], reverse=True
        )

        for similarity_score, idx in ranked_search_results:
            if similarity_score < similarity_threshold:
                break

            ontology_id: str = self._embedding_metadata[idx]

            if ontology_id in seen_ids:
                continue

            seen_ids.add(ontology_id)
            candidates.append(ontology_id)
            if len(candidates) >= max_candidates:
                break

        return candidates
