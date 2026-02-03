from hpotk import Ontology

from deft_matcher.matcher import Matcher
from deft_matcher.ontology_class import OntologyClass
from deft_matcher.utils import get_ontology_prefix, get_oc


class ExactMatcher(Matcher):
    """
    If the free text matches the primary label of an ontology term,
    the ontology ID is returned.
    """

    _ontology: Ontology
    _label_to_term: dict[str, OntologyClass]

    def __init__(self, ontology: Ontology) -> None:
        self._ontology = ontology
        self._label_to_term = self._initialise_label_to_term()

    def _initialise_label_to_term(self) -> dict[str, OntologyClass]:
        return {term.name.lower(): get_oc(term) for term in self._ontology.terms}

    @property
    def name(self) -> str:
        return f"ExactMatcher({get_ontology_prefix(self._ontology)})"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        possible_match = self._label_to_term.get(free_text.lower())
        return [] if possible_match is None else [possible_match]
