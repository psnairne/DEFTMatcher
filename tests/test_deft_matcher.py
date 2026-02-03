import hpotk
import pytest
import pandas as pd
import os

from hpotk import OntologyType

from deft_matcher.ambiguity_resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.deft_matcher import DeftMatcher
from deft_matcher.matchers.exact_matcher import ExactMatcher
from deft_matcher.matchers.fast_hpo_cr_matcher import FastHPOCRMatcher
from deft_matcher.matchers.fast_mondo_cr_matcher import FastMONDOCRMatcher
from deft_matcher.matchers.rag_hpo_matcher.rag_hpo_matcher import RagHpoMatcher
from deft_matcher.matchers.synonym_matcher import SynonymMatcher


@pytest.fixture
def store():
    return hpotk.configure_ontology_store()


@pytest.fixture
def hpo(store):
    return store.load_hpo(release="v2025-11-24")


@pytest.fixture
def mondo(store):
    return store.load_ontology(
        ontology_type=OntologyType.MONDO,
        release="v2025-12-02",
        prefixes_of_interest={"MONDO"},
    )


@pytest.fixture
def hpo_obo_path():
    return "/Users/patrick/Downloads/HPO_FILES/hp.obo"


@pytest.fixture
def mondo_obo_path():
    return "/Users/patrick/Downloads/MONDO_FILES/mondo.obo"


@pytest.fixture
def data_output_dir():
    return "/Users/patrick/DEFTMatcher/tests/data"


@pytest.fixture
def hpo_exact_matcher(hpo):
    return ExactMatcher(ontology=hpo)


@pytest.fixture
def hpo_syn_matcher(hpo):
    return SynonymMatcher(ontology=hpo)


@pytest.fixture
def mondo_exact_matcher(mondo):
    return ExactMatcher(ontology=mondo)


@pytest.fixture
def mondo_syn_matcher(mondo):
    return SynonymMatcher(ontology=mondo)


@pytest.fixture
def fast_hpo_cr_matcher(hpo_obo_path, data_output_dir):
    return FastHPOCRMatcher(hpo_obo_path=hpo_obo_path, data_output_dir=data_output_dir)


@pytest.fixture
def fast_mondo_cr_matcher(mondo_obo_path, data_output_dir):
    return FastMONDOCRMatcher(
        mondo_obo_path=mondo_obo_path, data_output_dir=data_output_dir
    )


@pytest.fixture
def rag_hpo_matcher():
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


@pytest.fixture
def choose_first():
    return ChooseFirstResolver()


@pytest.fixture
def conditions():
    dfs = pd.read_excel(
        "/Users/patrick/Downloads/PhenoXtract/i_data.xlsx", sheet_name=None
    )
    conditions_df = dfs["Conditions"]
    conditions_col = conditions_df["Condition"]
    return set(conditions_col)


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_deft_matcher_conditions_col(
    conditions,
    hpo_exact_matcher,
    hpo_syn_matcher,
    mondo_exact_matcher,
    mondo_syn_matcher,
    fast_hpo_cr_matcher,
    fast_mondo_cr_matcher,
    rag_hpo_matcher,
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

    rag_hpo_matcher_dm = DecisiveMatcher(
        matcher=rag_hpo_matcher, ambiguity_resolver=choose_first
    )

    conditions_normaliser = DeftMatcher(
        decisive_matchers=[
            hpo_exact_dm,
            hpo_syn_dm,
            fast_hpo_cr_dm,
            mondo_exact_dm,
            mondo_syn_dm,
            fast_mondo_cr_dm,
            rag_hpo_matcher_dm,
        ],
        free_texts=conditions,
        data_name="IDATA",
    )

    conditions_normaliser.run()
