from dataclasses import dataclass
from oaklib.interfaces import OboGraphInterface


@dataclass(frozen=True)
class OntologyClass:
    """
    A label and an ID.
    No validation is performed here, that should be done beforehand.
    """

    curie_id: str
    label: str

    @classmethod
    def from_term_id(cls, term_id: str, ontology: OboGraphInterface) -> "OntologyClass":
        label: str = ontology.label(term_id)
        return OntologyClass(term_id, label)
