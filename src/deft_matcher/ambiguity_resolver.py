from abc import ABC, abstractmethod


class AmbiguityResolver(ABC):
    """
    When a matcher returns a list of possible matches, the job of an AmbiguityResolver
    is to choose exactly one of those.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Each ambiguity resolver must have a 'name' attribute."""
        pass

    @abstractmethod
    def resolve(self, possible_matches: list[str]) -> str | None:
        """Given a list of possible matches for some free text, this function should choose exactly one of them."""
        raise NotImplementedError
