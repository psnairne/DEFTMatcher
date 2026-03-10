from deft_matcher.resolvers.choose_first_resolver import ChooseFirstResolver
from deft_matcher.ontology_class import OntologyClass


def test_choose_first_resolver():
    choose_first = ChooseFirstResolver()
    assert choose_first.resolve(
        [
            OntologyClass("HP:0000729", "Autistic behavior"),
            OntologyClass("HP:0001631", "Atrial septal defect"),
        ]
    ) == OntologyClass("HP:0000729", "Autistic behavior")
