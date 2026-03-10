from typing import Iterable

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface

from deft_matcher.retriever import Retriever
from deft_matcher.utils import validate_file_path_has_version_and_return
from deft_matcher.retrievers.vector_similarity_retriever.vector_embedder import (
    VectorEmbedder,
)
from deft_matcher.ontology_class import OntologyClass


class VectorSimilarityRetriever(Retriever):
    """
    Given an embeddings.npz file and a metadata.json file whose indexes agree with those of the embeddings,
    this retriever will retrieve candidate ontology terms based on a vector similarity search.

    Note: the version of the embedded ontology MUST agree with the version of the ontology used for Oaklib.
    """

    ontology_prefix: str
    ontology_obo_path: str
    root_term: str
    ontology_version: str
    _oak_ontology_str: str
    _ontology: OboGraphInterface
    _id_to_term: dict[str, OntologyClass]

    def __init__(
        self,
        ontology_prefix: str,
        ontology_obo_path: str,
        root_term: str,
        embedding_path: str,
        embedding_metadata_path: str,
        embedding_model_path: str,
        similarity_threshold: float = 0.8,
        max_candidates: int = 1,
    ) -> None:
        self.ontology_prefix = ontology_prefix
        self.ontology_obo_path = ontology_obo_path
        self.root_term = root_term
        self.embedding_path = embedding_path
        self.embedding_metadata_path = embedding_metadata_path
        self.embedding_model_path = embedding_model_path
        self._candidate_retriever = VectorEmbedder(
            embedding_path, embedding_metadata_path, embedding_model_path
        )
        self.similarity_threshold = similarity_threshold
        self.max_candidates = max_candidates
        self.ontology_version = validate_file_path_has_version_and_return(
            self.ontology_obo_path
        )
        self._oak_ontology_str = self._initialise_oak_ontology_str()
        self._ontology = self._initialise_ontology()
        self._id_to_term = self._initialise_id_to_term()

    def _initialise_oak_ontology_str(self) -> str:
        return "simpleobo:" + self.ontology_obo_path

    def _initialise_ontology(self) -> OboGraphInterface:
        return get_adapter(self._oak_ontology_str)

    def _initialise_id_to_term(self) -> dict[str, OntologyClass]:
        all_term_ids: Iterable[str] = self._ontology.descendants(
            self.root_term, predicates=[IS_A]
        )
        id_to_term: dict[str, OntologyClass] = dict()
        for term_id in all_term_ids:
            id_to_term[term_id] = OntologyClass.from_term_id(term_id, self._ontology)
        return id_to_term

    @property
    def name(self) -> str:
        return f"VectorSimilarityMatcher({self.ontology_prefix.upper()})"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        candidates: list[str] = self._candidate_retriever.get_most_similar(
            phrase=free_text,
            similarity_threshold=self.similarity_threshold,
            max_candidates=self.max_candidates,
        )

        return [self._id_to_term[candidate] for candidate in candidates]
