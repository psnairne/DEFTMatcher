import logging

import hpotk
from hpotk import OntologyStore, Ontology, OntologyType

from deft_matcher.ambiguity_resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.matchers.exact_matcher import ExactMatcher
from deft_matcher.matchers.fast_hpo_cr_matcher import FastHPOCRMatcher
from deft_matcher.matchers.fast_mondo_cr_matcher import FastMONDOCRMatcher
from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.human_matcher.user_interfaces.console_interface_hpo import (
    ConsoleInterfaceHpo,
)
from deft_matcher.matchers.null_matcher import NullMatcher
from deft_matcher.matchers.rag_hpo_matcher.rag_hpo_matcher import RagHpoMatcher
from deft_matcher.matchers.synonym_matcher import SynonymMatcher
from deft_matcher.matchers.vector_similarity_matcher import HpoVectorSimilarityMatcher

# ---PATHS---


def hpo_obo_path() -> str:
    return "/Users/patrick/Downloads/HPO_FILES/hp.obo"


def mondo_obo_path() -> str:
    return "/Users/patrick/Downloads/MONDO_FILES/mondo.obo"


def data_output_dir() -> str:
    return "/Users/patrick/DEFTMatcher/tests/data"


def embedded_hpo_path() -> str:
    return "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_embedded.npz"


def embedding_metadata_path() -> str:
    return "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_meta.json"


def embedding_model_path() -> str:
    return "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/sbert_model"


# ---ONTOLOGIES---


def store() -> OntologyStore:
    return hpotk.configure_ontology_store()


def hpo() -> Ontology:
    return store().load_hpo(release="v2025-11-24")


def mondo() -> Ontology:
    # silences noisy hpotk comments
    logging.getLogger("hpotk").setLevel(logging.ERROR)

    return store().load_ontology(
        ontology_type=OntologyType.MONDO,
        release="v2025-12-02",
        prefixes_of_interest={"MONDO"},
    )


# ---MATCHERS---


def hpo_exact_matcher() -> ExactMatcher:
    return ExactMatcher(ontology=hpo())


def hpo_syn_matcher() -> SynonymMatcher:
    return SynonymMatcher(ontology=hpo())


def mondo_exact_matcher() -> ExactMatcher:
    return ExactMatcher(ontology=mondo())


def mondo_syn_matcher() -> SynonymMatcher:
    return SynonymMatcher(ontology=mondo())


def fast_hpo_cr_matcher() -> FastHPOCRMatcher:
    return FastHPOCRMatcher(
        hpo_obo_path=hpo_obo_path(), data_output_dir=data_output_dir()
    )


def fast_mondo_cr_matcher() -> FastMONDOCRMatcher:
    return FastMONDOCRMatcher(
        mondo_obo_path=mondo_obo_path(), data_output_dir=data_output_dir()
    )


def rag_hpo_matcher() -> RagHpoMatcher:
    return RagHpoMatcher(
        model_name="llama3.2",
        embedded_hpo_path=embedded_hpo_path(),
        embedding_metadata_path=embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
    )


def vector_similarity_matcher() -> HpoVectorSimilarityMatcher:
    return HpoVectorSimilarityMatcher(
        embedded_hpo_path=embedded_hpo_path(),
        embedding_metadata_path=embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=0.75,
        max_candidates=1,
    )


def vector_similarity_matcher_five_candidates() -> HpoVectorSimilarityMatcher:
    return HpoVectorSimilarityMatcher(
        embedded_hpo_path=embedded_hpo_path(),
        embedding_metadata_path=embedding_metadata_path(),
        embedding_model_path=embedding_model_path(),
        similarity_threshold=0,
        max_candidates=5,
    )


def human_matcher() -> HumanMatcher:
    return HumanMatcher(
        ConsoleInterfaceHpo(hpo_version="v2025-11-24"),
        vector_similarity_matcher_five_candidates(),
    )


def null_matcher() -> NullMatcher:
    return NullMatcher()


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
        matcher=vector_similarity_matcher(), ambiguity_resolver=choose_first()
    )


def human_dm() -> DecisiveMatcher:
    return DecisiveMatcher(matcher=human_matcher(), ambiguity_resolver=choose_first())


def null_dm() -> DecisiveMatcher:
    return DecisiveMatcher(matcher=null_matcher(), ambiguity_resolver=choose_first())
