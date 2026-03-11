from oaklib.interfaces import OboGraphInterface

from deft_matcher.matcher import Matcher
from deft_matcher.ontology_class import OntologyClass
from deft_matcher.retrievers.vector_similarity_retriever.vector_similarity_retriever import (
    VectorSimilarityRetriever,
)


class VectorSimilarityMatcher(Matcher):
    """
    Given an embeddings.npz file and a metadata.json file whose indexes agree with those of the embeddings,
    this matcher will retrieve the best OntologyClass candidate based on a vector similarity search.

    Note: the version of the embedded ontology MUST agree with the version of the ontology used for Oaklib.
    """

    ontology_prefix: str
    ontology_obo_path: str
    root_term: str
    ontology_version: str
    _oak_ontology_str: str
    _ontology: OboGraphInterface
    _id_to_term: dict[str, OntologyClass]
    _vector_similarity_retriever: VectorSimilarityRetriever

    def __init__(
        self,
        ontology_prefix: str,
        ontology_obo_path: str,
        root_term: str,
        embedding_path: str,
        embedding_metadata_path: str,
        embedding_model_path: str,
        similarity_threshold: float = 0.8,
    ) -> None:
        self.ontology_prefix = ontology_prefix
        self.ontology_obo_path = ontology_obo_path
        self.root_term = root_term
        self.embedding_path = embedding_path
        self.embedding_metadata_path = embedding_metadata_path
        self.embedding_model_path = embedding_model_path
        self.similarity_threshold = similarity_threshold
        self._vector_similarity_retriever = VectorSimilarityRetriever(
            self.ontology_prefix,
            self.ontology_obo_path,
            self.root_term,
            self.embedding_path,
            self.embedding_metadata_path,
            self.embedding_model_path,
            self.similarity_threshold,
            1,
        )

    @property
    def name(self) -> str:
        return f"VectorSimilarityMatcher({self.ontology_prefix.upper()},{self.similarity_threshold})"

    def match(self, free_text: str) -> OntologyClass | None:
        candidates: list[OntologyClass] = self._vector_similarity_retriever.get_matches(
            free_text
        )
        return candidates[0] if candidates else None
