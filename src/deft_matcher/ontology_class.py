class OntologyClass:
    """
    A label and an ID.
    No validation is performed here, that should be done beforehand.
    """

    curie_id: str
    label: str

    def __init__(
        self,
        curie_id: str,
        label: str,
    ) -> None:
        self.curie_id = curie_id
        self.label = label
