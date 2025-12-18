import hpotk
import pytest
import pandas as pd

from deft_matcher.ambiguity_resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.deft_matcher import DeftMatcher
from deft_matcher.matchers.exact_matcher import ExactMatcher
from deft_matcher.matchers.synonym_matcher import SynonymMatcher


@pytest.fixture
def hpo():
    store = hpotk.configure_ontology_store()
    return store.load_hpo(release="v2025-11-24")


@pytest.fixture
def conditions():
    dfs = pd.read_excel(
        "/Users/patrick/Downloads/PhenoXtract/i_data.xlsx", sheet_name=None
    )
    conditions_df = dfs["Conditions"]
    conditions_col = conditions_df["Condition"]
    return set(conditions_col)


def test_deft_matcher_conditions_col(conditions, hpo):
    exact_matcher = ExactMatcher(ontology=hpo)
    synonym_matcher = SynonymMatcher(ontology=hpo)
    choose_first = ChooseFirstResolver()

    decisive_exact_matcher = DecisiveMatcher(
        matcher=exact_matcher, ambiguity_resolver=choose_first
    )
    decisive_synonym_matcher = DecisiveMatcher(
        matcher=synonym_matcher, ambiguity_resolver=choose_first
    )

    conditions_normaliser = DeftMatcher(
        decisive_matchers=[decisive_exact_matcher, decisive_synonym_matcher],
        free_texts=conditions,
        data_name="IDATA",
    )

    conditions_normaliser.next()
    conditions_normaliser.next()
