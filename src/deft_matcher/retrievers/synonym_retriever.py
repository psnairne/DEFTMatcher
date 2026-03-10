from typing import Iterable

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface

from deft_matcher.retriever import Retriever
from deft_matcher.utils import validate_file_path_has_version_and_return
from deft_matcher.ontology_class import OntologyClass


class SynonymRetriever(Retriever):
    """
    If a synonym of an ontology term matches the free text,
    then that term is added to the output of get_matches.
    """

    ontology_prefix: str
    ontology_obo_path: str
    root_term: str
    ontology_version: str
    _oak_ontology_str: str
    _ontology: OboGraphInterface
    _syn_to_terms: dict[str, list[OntologyClass]]

    def __init__(
        self, ontology_prefix: str, ontology_obo_path: str, root_term: str
    ) -> None:
        self.ontology_prefix = ontology_prefix
        self.ontology_obo_path = ontology_obo_path
        self.ontology_version = validate_file_path_has_version_and_return(
            self.ontology_obo_path
        )
        self.root_term = root_term
        self._oak_ontology_str = self._initialise_oak_ontology_str()
        self._ontology = self._initialise_ontology()
        self._syn_to_terms = self._initialise_syn_to_terms()

    def _initialise_oak_ontology_str(self) -> str:
        return "simpleobo:" + self.ontology_obo_path

    def _initialise_ontology(self) -> OboGraphInterface:
        return get_adapter(self._oak_ontology_str)

    def _initialise_syn_to_terms(self) -> dict[str, list[OntologyClass]]:
        """
        For each allowed synonym, returns all ontology IDs which correspond to it.
        Yes, it is possible that a synonym appears twice in an ontology.
        """

        all_term_ids: Iterable[str] = self._ontology.descendants(
            self.root_term, predicates=[IS_A]
        )

        syn_to_terms: dict[str, list[OntologyClass]] = {}

        for term_id in all_term_ids:
            synonyms: list[str] = self._ontology.entity_aliases(term_id)

            for syn in synonyms:
                syn_to_terms.setdefault(syn.lower(), []).append(
                    OntologyClass.from_term_id(term_id, self._ontology)
                )

        return syn_to_terms

    @property
    def name(self) -> str:
        return f"SynonymRetriever({self.ontology_prefix.upper()})"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        possible_matches = self._syn_to_terms.get(free_text.lower())
        return [] if possible_matches is None else possible_matches
