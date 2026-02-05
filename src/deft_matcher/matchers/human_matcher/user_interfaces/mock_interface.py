from deft_matcher.ontology_class import OntologyClass
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)


class MockInterface(UserInterface):
    """
    Acts as if the user always inputs OntologyClass("HP:0002099", "Asthma").
    """

    interface: UserInterface

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        return "MockInterface"

    def user_selection(
        self, free_text: str, candidates: list[OntologyClass]
    ) -> OntologyClass | None:
        return OntologyClass("HP:0002099", "Asthma")
