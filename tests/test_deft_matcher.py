from pathlib import Path
import pytest
import pandas as pd
import os
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import hpo_exact_dm


@pytest.fixture
def conditions() -> list[str]:
    dfs = pd.read_excel(
        "/Users/patrick/Downloads/PhenoXtract/i_data.xlsx", sheet_name=None
    )
    conditions_df = dfs["Conditions"]
    conditions_col = conditions_df["Condition"]
    return list(conditions_col)


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_deft_matcher_conditions_col(conditions):
    config = DeftMatcherConfig(decisive_matchers=[hpo_exact_dm()])

    data = DeftMatcherData(free_texts=conditions, data_name="IDATA")

    conditions_normaliser = DeftMatcher(config=config, data=data)

    conditions_normaliser.run()
    conditions_normaliser.output_results(
        Path("/Users/patrick/DEFTMatcher/tests/deft_matcher_output")
    )


# TODO there is no reason for this to be skipped in CI
@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_load_from_state():
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/deft_matcher_output/deft_matcher_results_8551dee1-3956-47d1-9499-e2cec9aedeeb_12-02-2026_17-06-15/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/deft_matcher_output/deft_matcher_results_8551dee1-3956-47d1-9499-e2cec9aedeeb_12-02-2026_17-06-15/metadata.json",
        decisive_matchers=[hpo_exact_dm()],
    )

    print(len(deft_matcher.matchings))
    print(len(deft_matcher.unmatched))
    print(len(deft_matcher.decisive_matchers))
