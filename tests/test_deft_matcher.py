import logging
from pathlib import Path

import pytest
import pandas as pd
import os

from hpotk import OntologyType, Ontology, OntologyStore

from deft_matcher.ambiguity_resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from deft_matcher.matchers.exact_matcher import ExactMatcher
from deft_matcher.matchers.fast_hpo_cr_matcher import FastHPOCRMatcher
from deft_matcher.matchers.fast_mondo_cr_matcher import FastMONDOCRMatcher
from deft_matcher.matchers.null_matcher import NullMatcher
from deft_matcher.matchers.synonym_matcher import SynonymMatcher
from deft_matcher.matchers.vector_similarity_matcher.vector_similarity_matcher import (
    VectorSimilarityMatcher,
)


@pytest.fixture
def hpo_obo_path() -> str:
    return (
        "/Users/patrick/DEFTMatcher/tests/assets/ontology_obo_files/hp_v2026-02-16.obo"
    )


@pytest.fixture
def mondo_obo_path() -> str:
    return "/Users/patrick/DEFTMatcher/tests/assets/ontology_obo_files/mondo_v2026-02-03.obo"


@pytest.fixture
def data_output_dir() -> str:
    return "/Users/patrick/DEFTMatcher/tests/assets/fast_hpo_cr_data"


@pytest.fixture
def hpo_exact_matcher(hpo_obo_path):
    return ExactMatcher(
        "hp",
        hpo_obo_path,
        # phenotypic abnormality
        "HP:0000118",
    )


@pytest.fixture
def hpo_syn_matcher(hpo_obo_path):
    return SynonymMatcher(
        "hp",
        hpo_obo_path,
        # phenotypic abnormality
        "HP:0000118",
    )


@pytest.fixture
def mondo_exact_matcher(mondo_obo_path):
    return ExactMatcher(
        "mondo",
        mondo_obo_path,
        # disease
        "HP:0000001",
    )


@pytest.fixture
def mondo_syn_matcher(mondo_obo_path):
    return SynonymMatcher(
        "mondo",
        mondo_obo_path,
        # disease
        "MONDO:0000001",
    )


@pytest.fixture
def fast_hpo_cr_matcher(hpo_obo_path, data_output_dir) -> FastHPOCRMatcher:
    return FastHPOCRMatcher(
        hpo_obo_path=hpo_obo_path,
        data_output_dir=data_output_dir,
        root_term="HP:0000001",
    )


@pytest.fixture
def fast_mondo_cr_matcher(mondo_obo_path, data_output_dir) -> FastMONDOCRMatcher:
    return FastMONDOCRMatcher(
        mondo_obo_path=mondo_obo_path,
        data_output_dir=data_output_dir,
        root_term="MONDO:0000001",
    )


@pytest.fixture
def vector_similarity_matcher(hpo_obo_path) -> VectorSimilarityMatcher:
    embedded_hpo_path = "/Users/patrick/DEFTMatcher/tests/assets/vector_similarity_matcher_data/data/hpo_embedded.npz"
    embedding_metadata_path = "/Users/patrick/DEFTMatcher/tests/assets/vector_similarity_matcher_data/data/hpo_meta.json"
    embedding_model_path = "/Users/patrick/DEFTMatcher/tests/assets/vector_similarity_matcher_data/sbert_model"
    return VectorSimilarityMatcher(
        embedding_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
        similarity_threshold=0.75,
        ontology_obo_path=hpo_obo_path,
        ontology_prefix="hp",
        root_term="HP:0000001",
    )


@pytest.fixture
def null_matcher() -> NullMatcher:
    return NullMatcher()


@pytest.fixture
def choose_first() -> ChooseFirstResolver:
    return ChooseFirstResolver()


@pytest.fixture
def conditions() -> list[str]:
    dfs = pd.read_excel(
        "/Users/patrick/Downloads/PhenoXtract/i_data.xlsx", sheet_name=None
    )
    conditions_df = dfs["Conditions"]
    conditions_col = conditions_df["Condition"]
    return list(conditions_col)


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_deft_matcher_conditions_col(
    conditions,
    hpo_exact_matcher,
    hpo_syn_matcher,
    mondo_exact_matcher,
    mondo_syn_matcher,
    fast_hpo_cr_matcher,
    fast_mondo_cr_matcher,
    vector_similarity_matcher,
    null_matcher,
    choose_first,
):
    hpo_exact_dm = DecisiveMatcher(
        matcher=hpo_exact_matcher, ambiguity_resolver=choose_first
    )
    hpo_syn_dm = DecisiveMatcher(
        matcher=hpo_syn_matcher, ambiguity_resolver=choose_first
    )

    fast_hpo_cr_dm = DecisiveMatcher(
        matcher=fast_hpo_cr_matcher, ambiguity_resolver=choose_first
    )

    mondo_exact_dm = DecisiveMatcher(
        matcher=mondo_exact_matcher, ambiguity_resolver=choose_first
    )
    mondo_syn_dm = DecisiveMatcher(
        matcher=mondo_syn_matcher, ambiguity_resolver=choose_first
    )

    fast_mondo_cr_dm = DecisiveMatcher(
        matcher=fast_mondo_cr_matcher, ambiguity_resolver=choose_first
    )

    vector_similarity_dm = DecisiveMatcher(
        matcher=vector_similarity_matcher, ambiguity_resolver=choose_first
    )

    null_dm = DecisiveMatcher(matcher=null_matcher, ambiguity_resolver=choose_first)

    config = DeftMatcherConfig(
        decisive_matchers=[
            hpo_exact_dm,
            hpo_syn_dm,
            fast_hpo_cr_dm,
            mondo_exact_dm,
            mondo_syn_dm,
            fast_mondo_cr_dm,
            vector_similarity_dm,
            null_dm,
        ]
    )

    data = DeftMatcherData(free_texts=conditions, data_name="IDATA")

    conditions_normaliser = DeftMatcher(config=config, data=data)

    conditions_normaliser.run()
    conditions_normaliser.output_results(
        Path("/Users/patrick/DEFTMatcher/tests/deft_matcher_output")
    )
