from typing import Iterable

from oaklib.interfaces import OboGraphInterface

from deft_matcher.matcher import Matcher
from deft_matcher.utils import validate_file_path_has_version_and_return
from deft_matcher.ontology_class import OntologyClass

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A


class ExactMatcher(Matcher):
    """
    If the free text matches the primary label of an ontology term,
    the ontology ID is returned.
    """

    ontology_prefix: str
    ontology_obo_path: str
    root_term: str
    ontology_version: str
    _oak_ontology_str: str
    _ontology: OboGraphInterface
    _label_to_term: dict[str, OntologyClass]

    def __init__(
        self, ontology_prefix: str, ontology_obo_path: str, root_term: str
    ) -> None:
        self.ontology_prefix = ontology_prefix
        self.ontology_obo_path = ontology_obo_path
        self.root_term = root_term
        self.ontology_version = validate_file_path_has_version_and_return(
            self.ontology_obo_path
        )
        self._oak_ontology_str = self._initialise_oak_ontology_str()
        self._ontology = self._initialise_ontology()
        self._label_to_term = self._initialise_label_to_term()

    def _initialise_oak_ontology_str(self) -> str:
        return "simpleobo:" + self.ontology_obo_path

    def _initialise_ontology(self) -> OboGraphInterface:
        return get_adapter(self._oak_ontology_str)

    def _initialise_label_to_term(self) -> dict[str, OntologyClass]:
        all_term_ids: Iterable[str] = self._ontology.descendants(
            self.root_term, predicates=[IS_A]
        )
        label_to_term: dict[str, OntologyClass] = dict()
        for term_id in all_term_ids:
            label: str = self._ontology.label(term_id)
            label_to_term[label.lower()] = OntologyClass.from_term_id(
                term_id, self._ontology
            )
        return label_to_term

    @property
    def name(self) -> str:
        return f"ExactMatcher({self.ontology_prefix.upper()})"

    def match(self, free_text: str) -> OntologyClass | None:
        return self._label_to_term.get(free_text.lower())
