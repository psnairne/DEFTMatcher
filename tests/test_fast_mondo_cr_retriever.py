import os

import pytest

from deft_matcher.retrievers.fast_mondo_cr_retriever import FastMONDOCRRetriever
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import mondo_obo_path, fast_hpo_cr_asset_dir


@pytest.mark.skipif(os.getenv("CI") == "true", reason="MONDO obo file too big")
def test_fast_mondo_cr_matcher():
    # NOTE: if you don't already have MONDO indexed, this will take about 20 mins

    fast_mondo_cr_matcher = FastMONDOCRRetriever(
        mondo_obo_path=mondo_obo_path(),
        data_output_dir=fast_hpo_cr_asset_dir(),
        root_term="MONDO:0000001",
    )

    assert fast_mondo_cr_matcher.get_matches(
        "cystic fibrosis and also nutritional disorder"
    ) == [
        OntologyClass("MONDO:0009061", "cystic fibrosis"),  # Asthma
        OntologyClass("MONDO:0005137", "nutritional disorder"),  # Short stature
    ]
