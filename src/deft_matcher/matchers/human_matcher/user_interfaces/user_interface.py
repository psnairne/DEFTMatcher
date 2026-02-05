from abc import ABC, abstractmethod

from deft_matcher.ontology_class import OntologyClass


class UserInterface(ABC):
    """
    A collection of methods needed by DEFTMatcher which should be provided by any UserInterface.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Each user interface must have a 'name' attribute."""
        pass

    @abstractmethod
    def user_selection(
        self, free_text: str, candidates: list[OntologyClass]
    ) -> OntologyClass | None:
        """Allows the user to select an OntologyClass."""
        raise NotImplementedError
