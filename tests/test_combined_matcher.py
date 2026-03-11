from deft_matcher.matchers.combined_matcher import CombinedMatcher
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_syn_retriever, choose_first_resolver


def test_combined_matcher():
    retriever = hpo_syn_retriever()
    resolver = choose_first_resolver()

    combined_matcher = CombinedMatcher(retriever, resolver)

    asd_match = combined_matcher.match("ASD")

    assert asd_match == OntologyClass(
        "HP:0000729", "Autistic behavior"
    ) or asd_match == OntologyClass("HP:0001631", "Atrial septal defect")
