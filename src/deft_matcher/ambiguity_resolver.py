from abc import ABC, abstractmethod
from typing import Optional


class AmbiguityResolver(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Each ambiguity resolver must have a 'name' attribute."""
        pass

    @abstractmethod
    def resolve(self, possible_matches: list[str]) -> Optional[str]:
        """Given a list of possible matches for some free text, this function should choose exactly one of them."""
        raise NotImplementedError
