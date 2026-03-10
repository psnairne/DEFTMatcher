from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_syn_retriever, maxo_syn_retriever


def test_synonym_matcher_hpo_success():
    asd_matches = hpo_syn_retriever().get_matches("ASD")

    assert len(asd_matches) == 2
    assert set(asd_matches) == {
        OntologyClass("HP:0000729", "Autistic behavior"),
        OntologyClass("HP:0001631", "Atrial septal defect"),
    }


def test_synonym_matcher_hpo_fail():
    asd_matches = hpo_syn_retriever().get_matches("OSD")

    assert len(asd_matches) == 0


def test_synonym_matcher_maxo():
    aorta_biopsy_matches = maxo_syn_retriever().get_matches("aorta biopsy")
    assert len(aorta_biopsy_matches) == 1
    assert set(aorta_biopsy_matches) == {
        OntologyClass("MAXO:0000333", "biopsy of aorta")
    }
