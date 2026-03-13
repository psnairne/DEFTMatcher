from abc import ABC, abstractmethod

from deft_matcher.ontology_class import OntologyClass


class Matcher(ABC):
    """
    The method match can match a free text to an OntologyClass. Or it can return None.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Each matcher must have a 'name' attribute."""
        pass

    @abstractmethod
    def match(self, free_text: str) -> OntologyClass | None:
        """Attempt to match the free text to an OntologyClass."""
        raise NotImplementedError
