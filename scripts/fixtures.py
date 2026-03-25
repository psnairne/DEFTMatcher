from deft_matcher.matchers.combined_matcher import CombinedMatcher
from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.vector_similarity_matcher import VectorSimilarityMatcher
from deft_matcher.resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.matchers.exact_matcher import ExactMatcher
from deft_matcher.retrievers.fast_hpo_cr_retriever import FastHPOCRRetriever
from deft_matcher.retrievers.fast_mondo_cr_retriever import FastMONDOCRRetriever
from deft_matcher.matchers.human_matcher.user_interfaces.console_interface import (
    ConsoleInterface,
)
from deft_matcher.matchers.null_matcher import NullMatcher
from deft_matcher.retrievers.synonym_retriever import SynonymRetriever
from deft_matcher.retrievers.vector_similarity_retriever.vector_similarity_retriever import (
    VectorSimilarityRetriever,
)
from scripts.utils import get_project_root_str


# ---PATHS---


def hpo_obo_path() -> str:
    return (
        get_project_root_str() + "/tests/assets/ontology_obo_files/hp_v2026-02-16.obo"
    )


def mondo_obo_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/ontology_obo_files/mondo_v2026-02-03.obo"
    )


def maxo_obo_path() -> str:
    return (
        get_project_root_str() + "/tests/assets/ontology_obo_files/maxo_v2026-01-15.obo"
    )


def hgnc_obo_path() -> str:
    return (
        get_project_root_str() + "/tests/assets/ontology_obo_files/hgnc_v2026-02-06.obo"
    )


def ncit_obo_path() -> str:
    return (
        get_project_root_str() + "/tests/assets/ontology_obo_files/ncit_v2026-03-19.obo"
    )


def fast_hpo_cr_asset_dir() -> str:
    return get_project_root_str() + "/tests/assets/fast_hpo_cr_data"


def hpo_embedding_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/hpo/hpo_embeddings.npz"
    )


def hpo_embedding_metadata_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/hpo/hpo_meta.json"
    )


def mondo_embedding_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/mondo/mondo_embeddings.npz"
    )


def mondo_embedding_metadata_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/mondo/mondo_meta.json"
    )


def maxo_embedding_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/maxo/maxo_embeddings.npz"
    )


def maxo_embedding_metadata_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/maxo/maxo_meta.json"
    )


def hgnc_embedding_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/hgnc/hgnc_embeddings.npz"
    )


def hgnc_embedding_metadata_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/hgnc/hgnc_meta.json"
    )


def ncit_embedding_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/ncit/ncit_embeddings.npz"
    )


def ncit_embedding_metadata_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/ncit/ncit_meta.json"
    )


def embedding_model_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/sbert_model"
    )


# ---RETRIEVERS---


def hpo_syn_retriever():
    return SynonymRetriever(
        "hp",
        hpo_obo_path(),
        # phenotypic abnormality
        "HP:0000118",
    )


def mondo_syn_retriever():
    return SynonymRetriever(
        "mondo",
        mondo_obo_path(),
        # disease
        "MONDO:0000001",
    )


def maxo_syn_retriever():
    return SynonymRetriever(
        "maxo",
        maxo_obo_path(),
        # medical action
        "MAXO:0000001",
    )


def hgnc_syn_retriever():
    return SynonymRetriever(
        "hgnc",
        hgnc_obo_path(),
        # protein coding gene
        "SO:0001217",
    )


def ncit_syn_retriever():
    return SynonymRetriever(
        "ncit",
        ncit_obo_path(),
        # root
        "NCIT:C14250",
    )


def fast_hpo_cr_retriever() -> FastHPOCRRetriever:
    return FastHPOCRRetriever(
        hpo_obo_path=hpo_obo_path(),
        data_output_dir=fast_hpo_cr_asset_dir(),
        # phenotypic abnormality
        root_term="HP:0000118",
    )


def fast_mondo_cr_retriever() -> FastMONDOCRRetriever:
    return FastMONDOCRRetriever(
        mondo_obo_path=mondo_obo_path(),
        data_output_dir=fast_hpo_cr_asset_dir(),
        # disease
        root_term="MONDO:0000001",
    )


def hpo_vec_similarity_retriever(
    similarity_threshold: float, number_of_candidates: int
) -> VectorSimilarityRetriever:
    return VectorSimilarityRetriever(
        embedding_path=hpo_embedding_path(),
        embedding_metadata_path=hpo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=similarity_threshold,
        max_candidates=number_of_candidates,
        ontology_obo_path=hpo_obo_path(),
        ontology_prefix="hp",
        # phenotypic abnormality
        root_term="HP:0000118",
    )


def mondo_vec_similarity_retriever(
    similarity_threshold: float, number_of_candidates: int
) -> VectorSimilarityRetriever:
    return VectorSimilarityRetriever(
        embedding_path=mondo_embedding_path(),
        embedding_metadata_path=mondo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=similarity_threshold,
        max_candidates=number_of_candidates,
        ontology_obo_path=mondo_obo_path(),
        ontology_prefix="mondo",
        # disease
        root_term="MONDO:0000001",
    )


def maxo_vec_similarity_retriever(
    similarity_threshold: float, number_of_candidates: int
) -> VectorSimilarityRetriever:
    return VectorSimilarityRetriever(
        embedding_path=maxo_embedding_path(),
        embedding_metadata_path=maxo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=similarity_threshold,
        max_candidates=number_of_candidates,
        ontology_obo_path=maxo_obo_path(),
        ontology_prefix="maxo",
        # medical action
        root_term="MAXO:0000001",
    )


def hgnc_vec_similarity_retriever(
    similarity_threshold: float, number_of_candidates: int
) -> VectorSimilarityRetriever:
    return VectorSimilarityRetriever(
        embedding_path=hgnc_embedding_path(),
        embedding_metadata_path=hgnc_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=similarity_threshold,
        max_candidates=number_of_candidates,
        ontology_obo_path=hgnc_obo_path(),
        ontology_prefix="hgnc",
        # protein coding gene
        root_term="SO:0001217",
    )


def ncit_vec_similarity_retriever(
    similarity_threshold: float, number_of_candidates: int
) -> VectorSimilarityRetriever:
    return VectorSimilarityRetriever(
        embedding_path=ncit_embedding_path(),
        embedding_metadata_path=ncit_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=similarity_threshold,
        max_candidates=number_of_candidates,
        ontology_obo_path=ncit_obo_path(),
        ontology_prefix="ncit",
        # organism
        root_term="NCIT:C14250",
    )


# ---RESOLVERS---


def choose_first_resolver() -> ChooseFirstResolver:
    return ChooseFirstResolver()


# ---MATCHERS---


def hpo_exact_matcher():
    return ExactMatcher(
        "hp",
        hpo_obo_path(),
        # phenotypic abnormality
        "HP:0000118",
    )


def mondo_exact_matcher():
    return ExactMatcher(
        "mondo",
        mondo_obo_path(),
        # disease
        "MONDO:0000001",
    )


def maxo_exact_matcher():
    return ExactMatcher(
        "maxo",
        maxo_obo_path(),
        # medical action
        "MAXO:0000001",
    )


def hgnc_exact_matcher():
    return ExactMatcher(
        "hgnc",
        hgnc_obo_path(),
        # protein coding gene
        "SO:0001217",
    )


def ncit_exact_matcher():
    return ExactMatcher(
        "ncit",
        ncit_obo_path(),
        # organism
        "NCIT:C14250",
    )


def hpo_vec_similarity_matcher(similarity_threshold: float) -> VectorSimilarityMatcher:
    return VectorSimilarityMatcher(
        embedding_path=hpo_embedding_path(),
        embedding_metadata_path=hpo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=similarity_threshold,
        ontology_obo_path=hpo_obo_path(),
        ontology_prefix="hp",
        # phenotypic abnormality
        root_term="HP:0000118",
    )


def mondo_vec_similarity_matcher(
    similarity_threshold: float,
) -> VectorSimilarityMatcher:
    return VectorSimilarityMatcher(
        embedding_path=mondo_embedding_path(),
        embedding_metadata_path=mondo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=similarity_threshold,
        ontology_obo_path=mondo_obo_path(),
        ontology_prefix="mondo",
        # disease
        root_term="MONDO:0000001",
    )


def maxo_vec_similarity_matcher(similarity_threshold: float) -> VectorSimilarityMatcher:
    return VectorSimilarityMatcher(
        embedding_path=maxo_embedding_path(),
        embedding_metadata_path=maxo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=similarity_threshold,
        ontology_obo_path=maxo_obo_path(),
        ontology_prefix="maxo",
        # medical action
        root_term="MAXO:0000001",
    )


def ncit_vec_similarity_matcher(similarity_threshold: float) -> VectorSimilarityMatcher:
    return VectorSimilarityMatcher(
        embedding_path=ncit_embedding_path(),
        embedding_metadata_path=ncit_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=similarity_threshold,
        ontology_obo_path=ncit_obo_path(),
        ontology_prefix="ncit",
        # organism
        root_term="NCIT:C14250",
    )


def hpo_human_matcher(number_of_candidates: int) -> HumanMatcher:
    return HumanMatcher(
        hpo_console_interface(),
        hpo_vec_similarity_retriever(
            similarity_threshold=0, number_of_candidates=number_of_candidates
        ),
    )


def mondo_human_matcher(number_of_candidates: int) -> HumanMatcher:
    return HumanMatcher(
        mondo_console_interface(),
        mondo_vec_similarity_retriever(
            similarity_threshold=0, number_of_candidates=number_of_candidates
        ),
    )


def hgnc_human_matcher(number_of_candidates: int) -> HumanMatcher:
    return HumanMatcher(
        hgnc_console_interface(),
        hgnc_vec_similarity_retriever(
            similarity_threshold=0, number_of_candidates=number_of_candidates
        ),
    )


def maxo_human_matcher(number_of_candidates: int) -> HumanMatcher:
    return HumanMatcher(
        maxo_console_interface(),
        maxo_vec_similarity_retriever(
            similarity_threshold=0, number_of_candidates=number_of_candidates
        ),
    )


def ncit_human_matcher(number_of_candidates: int) -> HumanMatcher:
    return HumanMatcher(
        ncit_console_interface(),
        ncit_vec_similarity_retriever(
            similarity_threshold=0, number_of_candidates=number_of_candidates
        ),
    )


def null_matcher() -> NullMatcher:
    return NullMatcher()


# ---USER_INTERFACES---


def hpo_console_interface() -> ConsoleInterface:
    return ConsoleInterface(
        ontology_prefix="hp",
        ontology_obo_path=hpo_obo_path(),
        # phenotypic abnormality
        root_term="HP:0000118",
    )


def mondo_console_interface() -> ConsoleInterface:
    return ConsoleInterface(
        ontology_prefix="mondo",
        ontology_obo_path=mondo_obo_path(),
        # disease
        root_term="MONDO:0000001",
    )


def maxo_console_interface() -> ConsoleInterface:
    return ConsoleInterface(
        ontology_prefix="maxo",
        ontology_obo_path=maxo_obo_path(),
        # medical action
        root_term="MAXO:0000001",
    )


def hgnc_console_interface() -> ConsoleInterface:
    return ConsoleInterface(
        ontology_prefix="hgnc",
        ontology_obo_path=hgnc_obo_path(),
        # protein coding gene
        root_term="SO:0001217",
    )


def ncit_console_interface() -> ConsoleInterface:
    return ConsoleInterface(
        ontology_prefix="ncit",
        ontology_obo_path=ncit_obo_path(),
        # organism
        root_term="NCIT:C14250",
    )


# ---COMBINED_MATCHERS---


def hpo_syn_matcher() -> CombinedMatcher:
    return CombinedMatcher(
        hpo_syn_retriever(), choose_first_resolver(), "SynonymMatcher(HP)"
    )


def mondo_syn_matcher() -> CombinedMatcher:
    return CombinedMatcher(
        mondo_syn_retriever(), choose_first_resolver(), "SynonymMatcher(MONDO)"
    )


def maxo_syn_matcher() -> CombinedMatcher:
    return CombinedMatcher(
        maxo_syn_retriever(), choose_first_resolver(), "SynonymMatcher(MAXO)"
    )


def hgnc_syn_matcher() -> CombinedMatcher:
    return CombinedMatcher(
        hgnc_syn_retriever(), choose_first_resolver(), "SynonymMatcher(HGNC)"
    )


def ncit_syn_matcher() -> CombinedMatcher:
    return CombinedMatcher(
        ncit_syn_retriever(), choose_first_resolver(), "SynonymMatcher(NCIT)"
    )


def fast_hpo_cr_matcher() -> CombinedMatcher:
    return CombinedMatcher(
        fast_hpo_cr_retriever(), choose_first_resolver(), "FastHPOCRMatcher"
    )


def fast_mondo_cr_matcher() -> CombinedMatcher:
    return CombinedMatcher(
        fast_mondo_cr_retriever(), choose_first_resolver(), "FastMONDOCRMatcher"
    )
