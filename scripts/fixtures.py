from deft_matcher.matchers.combined_matcher import CombinedMatcher
from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.vector_similarity_matcher import VectorSimilarityMatcher
from deft_matcher.resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.matcher import Matcher
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


def hpo_vec_similarity_retriever() -> VectorSimilarityRetriever:
    return VectorSimilarityRetriever(
        embedding_path=hpo_embedding_path(),
        embedding_metadata_path=hpo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=0,
        max_candidates=5,
        ontology_obo_path=hpo_obo_path(),
        ontology_prefix="hp",
        # phenotypic abnormality
        root_term="HP:0000118",
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
        "HP:0000001",
    )


def maxo_exact_matcher():
    return ExactMatcher(
        "maxo",
        maxo_obo_path(),
        # medical action
        "MAXO:0000001",
    )


def hpo_vec_similarity_matcher() -> VectorSimilarityMatcher:
    return VectorSimilarityMatcher(
        embedding_path=hpo_embedding_path(),
        embedding_metadata_path=hpo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=0.6,
        ontology_obo_path=hpo_obo_path(),
        ontology_prefix="hp",
        # phenotypic abnormality
        root_term="HP:0000118",
    )


def hpo_human_matcher() -> HumanMatcher:
    return HumanMatcher(hpo_console_interface(), hpo_vec_similarity_retriever())


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


# ---COMBINED_MATCHERS---


def hpo_syn_matcher() -> Matcher:
    return CombinedMatcher(hpo_syn_retriever(), choose_first_resolver())


def mondo_syn_matcher() -> Matcher:
    return CombinedMatcher(mondo_syn_retriever(), choose_first_resolver())


def fast_hpo_cr_matcher() -> Matcher:
    return CombinedMatcher(fast_hpo_cr_retriever(), choose_first_resolver())


def fast_mondo_cr_matcher() -> Matcher:
    return CombinedMatcher(fast_mondo_cr_retriever(), choose_first_resolver())
