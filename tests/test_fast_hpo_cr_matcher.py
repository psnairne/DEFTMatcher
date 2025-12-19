import os

import pytest

from deft_matcher.matchers.fast_hpo_cr_matcher import FastHPOCRMatcher


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_fast_hpo_cr_matcher():

    fast_hpo_cr_matcher = FastHPOCRMatcher(
        hpo_obo_path="/Users/patrick/Downloads/HPO_FILES/hp.obo",
        data_output_dir="/Users/patrick/DEFTMatcher/tests/data",
    )

    assert fast_hpo_cr_matcher.get_matches("asthma and shortened stature") == [
        "HP:0002099",  # Asthma
        "HP:0004322",  # Short stature
    ]
