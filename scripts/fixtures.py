from deft_matcher.ambiguity_resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.matchers.exact_matcher import ExactMatcher
from deft_matcher.matchers.fast_hpo_cr_matcher import FastHPOCRMatcher
from deft_matcher.matchers.fast_mondo_cr_matcher import FastMONDOCRMatcher
from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.human_matcher.user_interfaces.console_interface import (
    ConsoleInterface,
)
from deft_matcher.matchers.null_matcher import NullMatcher
from deft_matcher.matchers.synonym_matcher import SynonymMatcher
from deft_matcher.matchers.vector_similarity_matcher.vector_similarity_matcher import (
    VectorSimilarityMatcher,
)
from scripts.utils import get_project_root_str


# ---PATHS---


def hpo_obo_path() -> str:
    print(get_project_root_str())
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


def embedded_hpo_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/hpo/hpo_embeddings.npz"
    )


def hpo_embedding_metadata_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/hpo/hpo_meta.json"
    )


def embedded_mondo_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/mondo/mondo_embeddings.npz"
    )


def mondo_embedding_metadata_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/mondo/mondo_meta.json"
    )


def embedding_model_path() -> str:
    return (
        get_project_root_str()
        + "/tests/assets/vector_similarity_matcher_data/sbert_model"
    )


# ---MATCHERS---


def hpo_exact_matcher():
    return ExactMatcher(
        "hp",
        hpo_obo_path(),
        # phenotypic abnormality
        "HP:0000118",
    )


def hpo_syn_matcher():
    return SynonymMatcher(
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


def mondo_syn_matcher():
    return SynonymMatcher(
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


def maxo_syn_matcher():
    return SynonymMatcher(
        "maxo",
        maxo_obo_path(),
        # medical action
        "MAXO:0000001",
    )


def fast_hpo_cr_matcher() -> FastHPOCRMatcher:
    return FastHPOCRMatcher(
        hpo_obo_path=hpo_obo_path(),
        data_output_dir=fast_hpo_cr_asset_dir(),
        # phenotypic abnormality
        root_term="HP:0000118",
    )


def fast_mondo_cr_matcher() -> FastMONDOCRMatcher:
    return FastMONDOCRMatcher(
        mondo_obo_path=mondo_obo_path(),
        data_output_dir=fast_hpo_cr_asset_dir(),
        # disease
        root_term="MONDO:0000001",
    )


def hpo_vector_similarity_matcher() -> VectorSimilarityMatcher:
    return VectorSimilarityMatcher(
        embedding_path=embedded_hpo_path(),
        embedding_metadata_path=hpo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=0.6,
        max_candidates=1,
        ontology_obo_path=hpo_obo_path(),
        ontology_prefix="hp",
        # phenotypic abnormality
        root_term="HP:0000118",
    )


def hpo_candidate_retriever() -> VectorSimilarityMatcher:
    return VectorSimilarityMatcher(
        embedding_path=embedded_hpo_path(),
        embedding_metadata_path=hpo_embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=0,
        max_candidates=5,
        ontology_obo_path=hpo_obo_path(),
        ontology_prefix="hp",
        # phenotypic abnormality
        root_term="HP:0000118",
    )


def human_matcher_hpo() -> HumanMatcher:
    return HumanMatcher(hpo_console_interface(), hpo_candidate_retriever())


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


# ---RESOLVERS---


def choose_first() -> ChooseFirstResolver:
    return ChooseFirstResolver()


# ---DECISIVE_MATCHERS---


def hpo_exact_dm() -> DecisiveMatcher:
    return DecisiveMatcher(
        matcher=hpo_exact_matcher(), ambiguity_resolver=choose_first()
    )


def hpo_syn_dm() -> DecisiveMatcher:
    return DecisiveMatcher(matcher=hpo_syn_matcher(), ambiguity_resolver=choose_first())


def fast_hpo_cr_dm() -> DecisiveMatcher:
    return DecisiveMatcher(
        matcher=fast_hpo_cr_matcher(), ambiguity_resolver=choose_first()
    )


def mondo_exact_dm() -> DecisiveMatcher:
    return DecisiveMatcher(
        matcher=mondo_exact_matcher(), ambiguity_resolver=choose_first()
    )


def mondo_syn_dm() -> DecisiveMatcher:
    return DecisiveMatcher(
        matcher=mondo_syn_matcher(), ambiguity_resolver=choose_first()
    )


def fast_mondo_cr_dm() -> DecisiveMatcher:
    return DecisiveMatcher(
        matcher=fast_mondo_cr_matcher(), ambiguity_resolver=choose_first()
    )


def vector_similarity_dm() -> DecisiveMatcher:
    return DecisiveMatcher(
        matcher=hpo_vector_similarity_matcher(), ambiguity_resolver=choose_first()
    )


def human_dm_hpo() -> DecisiveMatcher:
    return DecisiveMatcher(
        matcher=human_matcher_hpo(), ambiguity_resolver=choose_first()
    )


def null_dm() -> DecisiveMatcher:
    return DecisiveMatcher(matcher=null_matcher(), ambiguity_resolver=choose_first())
