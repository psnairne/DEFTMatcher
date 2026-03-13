from abc import ABC, abstractmethod

from deft_matcher.ontology_class import OntologyClass


class Retriever(ABC):
    """
    Matches a free text to a list of possible OntologyClass candidates.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Each retriever must have a 'name' attribute."""
        pass

    @abstractmethod
    def get_matches(self, free_text: str) -> list[OntologyClass]:
        """Return matching ontology IDs for the given free text."""
        raise NotImplementedError
