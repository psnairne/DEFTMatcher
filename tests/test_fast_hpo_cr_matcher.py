from deft_matcher.matchers.fast_hpo_cr_matcher import FastHPOCRMatcher
from deft_matcher.ontology_class import OntologyClass


def test_fast_hpo_cr_matcher():
    fast_hpo_cr_matcher = FastHPOCRMatcher(
        hpo_obo_path="assets/ontology_obo_files/hp_v2026-02-16.obo",
        root_term="HP:0000118",
        data_output_dir="assets/fast_hpo_cr_data",
    )

    assert fast_hpo_cr_matcher.get_matches("asthma and shortened stature") == [
        OntologyClass("HP:0002099", "Asthma"),  # Asthma
        OntologyClass("HP:0004322", "Short stature"),  # Short stature
    ]
