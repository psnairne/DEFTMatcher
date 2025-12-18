import hpotk
import pytest
import pandas as pd

from free_text_normaliser.ambiguity_resolvers.choose_first_resolver import ChooseFirst
from free_text_normaliser.decisive_matcher import DecisiveMatcher
from free_text_normaliser.free_text_normaliser import FreeTextNormaliser
from free_text_normaliser.matchers.exact_matcher import ExactMatcher
from free_text_normaliser.matchers.synonym_matcher import SynonymMatcher


@pytest.fixture
def hpo():
    store = hpotk.configure_ontology_store()
    return store.load_hpo(release="v2025-11-24")


@pytest.fixture
def conditions():
    dfs = pd.read_excel(
        "/Users/patrick/Downloads/PhenoXtract/old_registry_data.xlsx", sheet_name=None
    )
    conditions_df = dfs["Conditions"]
    conditions_col = conditions_df["Condition"]
    return set(conditions_col)


def test_free_text_normaliser_conditions_col(conditions, hpo):
    exact_matcher = ExactMatcher(ontology=hpo)
    synonym_matcher = SynonymMatcher(ontology=hpo)
    choose_first = ChooseFirst()

    decisive_exact_matcher = DecisiveMatcher(
        matcher=exact_matcher, ambiguity_resolver=choose_first
    )
    decisive_synonym_matcher = DecisiveMatcher(
        matcher=synonym_matcher, ambiguity_resolver=choose_first
    )

    conditions_normaliser = FreeTextNormaliser(
        decisive_matchers=[decisive_exact_matcher, decisive_synonym_matcher],
        free_texts=conditions,
    )

    conditions_normaliser.next()
    conditions_normaliser.next()
