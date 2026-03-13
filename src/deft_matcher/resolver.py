from abc import ABC, abstractmethod

from deft_matcher.ontology_class import OntologyClass


class Resolver(ABC):
    """
    When a matcher returns a list of possible matches, the job of an Resolver
    is to choose exactly one of those.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Each resolver must have a 'name' attribute."""
        pass

    @abstractmethod
    def resolve(self, possible_matches: list[OntologyClass]) -> OntologyClass | None:
        """Given a list of possible matches for some free text, this function should choose exactly one of them."""
        raise NotImplementedError
