from dataclasses import dataclass

from hpotk import MinimalTerm
from hpotk import TermId


@dataclass(frozen=True)
class OntologyClass:
    """
    A label and an ID.
    No validation is performed here, that should be done beforehand.
    """

    curie_id: str
    label: str

    @classmethod
    def from_minimal_term(cls, minimal_term: "MinimalTerm") -> "OntologyClass":
        return OntologyClass(minimal_term.identifier.value, minimal_term.name)
