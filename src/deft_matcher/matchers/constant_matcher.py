from deft_matcher.matcher import Matcher
from deft_matcher.ontology_class import OntologyClass


class ConstantMatcher(Matcher):
    """
    Matches the free text to a chosen OntologyClass.
    """

    ontology_class: OntologyClass

    def __init__(self, ontology_class: OntologyClass) -> None:
        self.ontology_class = ontology_class

    @property
    def name(self) -> str:
        return f"ConstantMatcher({self.ontology_class.curie_id},{self.ontology_class.label})"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        return [self.ontology_class]
