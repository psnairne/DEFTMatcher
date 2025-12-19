from hpotk import Ontology, SynonymCategory, SynonymType

from deft_matcher.matcher import Matcher
from deft_matcher.utils import get_ontology_prefix


class SynonymMatcher(Matcher):
    """
    If a synonym of an ontology term matches the free text,
    then that synonym is added to the output of get_matches.

    The acceptable Synonym Categories and Types can be chosen.
    If synonym_categories or synonym_types = None, then that will be interpreted as "anything goes".
    """

    _ontology: Ontology
    _syn_to_ids: dict[str, list[str]]
    _allowed_synonym_categories: list[SynonymCategory]
    _allowed_synonym_types: list[SynonymType]

    def __init__(
        self,
        ontology: Ontology,
        synonym_categories: list[SynonymCategory] | None = None,
        synonym_types: list[SynonymType] | None = None,
    ) -> None:
        self._ontology = ontology
        self._allowed_synonym_categories = self._get_allowed_synonym_categories(
            synonym_categories
        )
        self._allowed_synonym_types = self._get_allowed_synonym_types(synonym_types)
        self._syn_to_ids = self._initialise_syn_to_ids()

    def _initialise_syn_to_ids(self) -> dict[str, list[str]]:
        """
        For each allowed synonym, returns all ontology IDs which correspond to it.
        Yes, it is possible that a synonym appears twice in an ontology.
        """

        syn_to_ids = {}

        for term in self._ontology.terms:
            if term.synonyms is None:
                continue

            for syn in term.synonyms:
                if (
                    syn.category in self._allowed_synonym_categories
                    and syn.synonym_type in self._allowed_synonym_types
                ):
                    syn_to_ids.setdefault(syn.name.lower(), []).append(
                        term.identifier.value
                    )

        return syn_to_ids

    @staticmethod
    def _get_allowed_synonym_categories(
        provided_synonym_categories: list[SynonymCategory | None] | None,
    ) -> list[SynonymCategory]:
        all_synonym_categories = [
            SynonymCategory.BROAD,
            SynonymCategory.NARROW,
            SynonymCategory.RELATED,
            SynonymCategory.EXACT,
            None,
        ]
        return (
            all_synonym_categories
            if provided_synonym_categories is None
            else provided_synonym_categories
        )

    @staticmethod
    def _get_allowed_synonym_types(
        provided_synonym_types: list[SynonymType | None] | None,
    ) -> list[SynonymType]:
        all_synonym_types = [
            SynonymType.OBSOLETE_SYNONYM,
            SynonymType.LAYPERSON_TERM,
            SynonymType.ABBREVIATION,
            SynonymType.ALLELIC_REQUIREMENT,
            SynonymType.PLURAL_FORM,
            SynonymType.UK_SPELLING,
            None,
        ]
        return (
            all_synonym_types
            if provided_synonym_types is None
            else provided_synonym_types
        )

    @property
    def name(self) -> str:
        return f"SynonymMatcher({get_ontology_prefix(self._ontology)})"

    def get_matches(self, free_text: str) -> list[str]:
        possible_matches = self._syn_to_ids.get(free_text.lower())
        return [] if possible_matches is None else possible_matches
