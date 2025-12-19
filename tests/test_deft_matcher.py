import hpotk
import pytest
import pandas as pd
import os

from hpotk import OntologyType

from deft_matcher.ambiguity_resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.deft_matcher import DeftMatcher
from deft_matcher.matchers.exact_matcher import ExactMatcher
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
def conditions():
    dfs = pd.read_excel(
        "/Users/patrick/Downloads/PhenoXtract/i_data.xlsx", sheet_name=None
    )
    conditions_df = dfs["Conditions"]
    conditions_col = conditions_df["Condition"]
    return set(conditions_col)


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_deft_matcher_conditions_col(conditions, hpo, mondo):

    hpo_exact_matcher = ExactMatcher(ontology=hpo)
    hpo_syn_matcher = SynonymMatcher(ontology=hpo)

    mondo_exact_matcher = ExactMatcher(ontology=mondo)
    mondo_syn_matcher = SynonymMatcher(ontology=mondo)

    choose_first = ChooseFirstResolver()

    hpo_exact_dm = DecisiveMatcher(
        matcher=hpo_exact_matcher, ambiguity_resolver=choose_first
    )
    hpo_syn_dm = DecisiveMatcher(
        matcher=hpo_syn_matcher, ambiguity_resolver=choose_first
    )
    mondo_exact_dm = DecisiveMatcher(
        matcher=mondo_exact_matcher, ambiguity_resolver=choose_first
    )
    mondo_syn_dm = DecisiveMatcher(
        matcher=mondo_syn_matcher, ambiguity_resolver=choose_first
    )

    conditions_normaliser = DeftMatcher(
        decisive_matchers=[hpo_exact_dm, hpo_syn_dm, mondo_exact_dm, mondo_syn_dm],
        free_texts=conditions,
        data_name="IDATA",
    )

    conditions_normaliser.run()
