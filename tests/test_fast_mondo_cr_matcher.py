import os

import pytest

from deft_matcher.matchers.fast_mondo_cr_matcher import FastMONDOCRMatcher


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_fast_mondo_cr_matcher():

    # NOTE: if you don't already have MONDO indexed, this will take about 20 mins

    fast_mondo_cr_matcher = FastMONDOCRMatcher(
        mondo_obo_path="/Users/patrick/Downloads/MONDO_FILES/mondo.obo",
        data_output_dir="/Users/patrick/DEFTMatcher/tests/data",
    )

    assert fast_mondo_cr_matcher.get_matches(
        "cystic fibrosis and other conditions"
    ) == [
        "MONDO:0009061",  # cystic fibrosis
        "MONDO:0000001",  # disease
    ]
