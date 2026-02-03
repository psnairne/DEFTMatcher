from dataclasses import dataclass


@dataclass(frozen=True)
class OntologyClass:
    """
    A label and an ID.
    No validation is performed here, that should be done beforehand.
    """

    curie_id: str
    label: str


# Then update tests
# Then implement vector similarity search for HPO and MONDO
# Then do proper CSV and logging output
# Then do HumanMatcher
