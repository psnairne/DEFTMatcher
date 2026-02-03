from dataclasses import dataclass


@dataclass(frozen=True)
class OntologyClass:
    """
    A label and an ID.
    No validation is performed here, that should be done beforehand.
    """

    curie_id: str
    label: str
