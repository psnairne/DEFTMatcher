import os

import pytest

from deft_matcher.matchers.fast_mondo_cr_matcher import FastMONDOCRMatcher
from deft_matcher.ontology_class import OntologyClass


@pytest.mark.skipif(os.getenv("CI") == "true", reason="MONDO obo file too big")
def test_fast_mondo_cr_matcher():
    # NOTE: if you don't already have MONDO indexed, this will take about 20 mins

    fast_mondo_cr_matcher = FastMONDOCRMatcher(
        mondo_obo_path="assets/ontology_obo_files/mondo_v2026-02-03.obo",
        data_output_dir="assets/fast_hpo_cr_data",
        root_term="MONDO:0000001",
    )

    assert fast_mondo_cr_matcher.get_matches(
        "cystic fibrosis and also nutritional disorder"
    ) == [
        OntologyClass("MONDO:0009061", "cystic fibrosis"),  # Asthma
        OntologyClass("MONDO:0005137", "nutritional disorder"),  # Short stature
    ]
