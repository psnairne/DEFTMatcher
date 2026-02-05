import logging
from pathlib import Path

import hpotk
import pandas as pd

from hpotk import OntologyType, Ontology, OntologyStore

from deft_matcher.ambiguity_resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from deft_matcher.matchers.exact_matcher import ExactMatcher
from deft_matcher.matchers.fast_hpo_cr_matcher import FastHPOCRMatcher
from deft_matcher.matchers.fast_mondo_cr_matcher import FastMONDOCRMatcher
from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.human_matcher.user_interfaces.console_interface import (
    ConsoleInterface,
)
from deft_matcher.matchers.null_matcher import NullMatcher
from deft_matcher.matchers.rag_hpo_matcher.rag_hpo_matcher import RagHpoMatcher
from deft_matcher.matchers.vector_similarity_matcher import HpoVectorSimilarityMatcher
from deft_matcher.matchers.synonym_matcher import SynonymMatcher


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


def hpo_obo_path() -> str:
    return "/Users/patrick/Downloads/HPO_FILES/hp.obo"


def mondo_obo_path() -> str:
    return "/Users/patrick/Downloads/MONDO_FILES/mondo.obo"


def data_output_dir() -> str:
    return "/Users/patrick/DEFTMatcher/tests/data"


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
    model_name = "llama3.2"
    embedded_hpo_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_embedded.npz"
    embedding_metadata_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_meta.json"
    embedding_model_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/sbert_model"
    return RagHpoMatcher(
        model_name=model_name,
        embedded_hpo_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
    )


def vector_similarity_matcher() -> HpoVectorSimilarityMatcher:
    embedded_hpo_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_embedded.npz"
    embedding_metadata_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_meta.json"
    embedding_model_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/sbert_model"
    return HpoVectorSimilarityMatcher(
        embedded_hpo_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
        similarity_threshold=0.75,
        max_candidates=1,
    )


def vector_similarity_matcher_ten_candidates() -> HpoVectorSimilarityMatcher:
    embedded_hpo_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_embedded.npz"
    embedding_metadata_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_meta.json"
    embedding_model_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/sbert_model"
    return HpoVectorSimilarityMatcher(
        embedded_hpo_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
        similarity_threshold=0,
        max_candidates=10,
    )


def human_matcher() -> HumanMatcher:
    return HumanMatcher(ConsoleInterface(), vector_similarity_matcher_ten_candidates())


def null_matcher() -> NullMatcher:
    return NullMatcher()


def choose_first() -> ChooseFirstResolver:
    return ChooseFirstResolver()


def conditions() -> list[str]:
    dfs = pd.read_excel(
        "/Users/patrick/Downloads/PhenoXtract/i_data.xlsx", sheet_name=None
    )
    conditions_df = dfs["Conditions"]
    conditions_col = conditions_df["Condition"]
    return list(conditions_col)


def main():
    hpo_exact_dm = DecisiveMatcher(
        matcher=hpo_exact_matcher(), ambiguity_resolver=choose_first()
    )
    hpo_syn_dm = DecisiveMatcher(
        matcher=hpo_syn_matcher(), ambiguity_resolver=choose_first()
    )

    fast_hpo_cr_dm = DecisiveMatcher(
        matcher=fast_hpo_cr_matcher(), ambiguity_resolver=choose_first()
    )

    mondo_exact_dm = DecisiveMatcher(
        matcher=mondo_exact_matcher(), ambiguity_resolver=choose_first()
    )
    mondo_syn_dm = DecisiveMatcher(
        matcher=mondo_syn_matcher(), ambiguity_resolver=choose_first()
    )

    fast_mondo_cr_dm = DecisiveMatcher(
        matcher=fast_mondo_cr_matcher(), ambiguity_resolver=choose_first()
    )

    vector_similarity_dm = DecisiveMatcher(
        matcher=vector_similarity_matcher(), ambiguity_resolver=choose_first()
    )

    human_matcher_dm = DecisiveMatcher(
        matcher=human_matcher(), ambiguity_resolver=choose_first()
    )

    null_dm = DecisiveMatcher(matcher=null_matcher(), ambiguity_resolver=choose_first())

    config = DeftMatcherConfig(
        decisive_matchers=[
            hpo_exact_dm,
            hpo_syn_dm,
            fast_hpo_cr_dm,
            mondo_exact_dm,
            mondo_syn_dm,
            fast_mondo_cr_dm,
            vector_similarity_dm,
            human_matcher_dm,
            null_dm,
        ]
    )

    data = DeftMatcherData(free_texts=conditions(), data_name="IDATA")

    conditions_normaliser = DeftMatcher(config=config, data=data)

    conditions_normaliser.run()
    conditions_normaliser.output_results(
        Path("/Users/patrick/DEFTMatcher/tests/deft_matcher_output")
    )


if __name__ == "__main__":
    main()
