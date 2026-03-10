import os

import pytest

from deft_matcher.retrievers.fast_hpo_cr_retriever import FastHPOCRRetriever
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_obo_path, fast_hpo_cr_asset_dir


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Index file too big")
def test_fast_hpo_cr_matcher():
    fast_hpo_cr_matcher = FastHPOCRRetriever(
        hpo_obo_path=hpo_obo_path(),
        root_term="HP:0000118",
        data_output_dir=fast_hpo_cr_asset_dir(),
    )

    assert fast_hpo_cr_matcher.get_matches("asthma and shortened stature") == [
        OntologyClass("HP:0002099", "Asthma"),  # Asthma
        OntologyClass("HP:0004322", "Short stature"),  # Short stature
    ]
