from hpotk import Ontology

from deft_matcher.matcher import Matcher
from deft_matcher.utils import get_ontology_prefix


class ExactMatcher(Matcher):
    """
    If the free text matches the primary label of an ontology term,
    the ontology ID is returned.
    """

    _ontology: Ontology
    _label_to_id: dict[str, str]

    def __init__(self, ontology: Ontology) -> None:
        self._ontology = ontology
        self._label_to_id = self._initialise_label_to_id()

    def _initialise_label_to_id(self) -> dict[str, str]:
        return {
            term.name.lower(): term.identifier.value for term in self._ontology.terms
        }

    @property
    def name(self) -> str:
        return f"ExactMatcher({get_ontology_prefix(self._ontology)})"

    def get_matches(self, free_text: str) -> list[str]:
        possible_match = self._label_to_id.get(free_text.lower())
        return [] if possible_match is None else [possible_match]
