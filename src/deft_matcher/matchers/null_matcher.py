from deft_matcher.matcher import Matcher
from deft_matcher.ontology_class import OntologyClass


class NullMatcher(Matcher):
    """
    Matches the free text to the null OntologyClass.
    """

    null_ontology_class: OntologyClass

    def __init__(self) -> None:
        self.null_ontology_class = OntologyClass("", "")

    @property
    def name(self) -> str:
        return "NullMatcher"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        return [self.null_ontology_class]
