from abc import ABC, abstractmethod


class Matcher(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Each matcher must have a 'name' attribute."""
        pass

    @abstractmethod
    def get_matches(self, free_text: str) -> list[str]:
        """Return matching ontology IDs for the given free text."""
        raise NotImplementedError
