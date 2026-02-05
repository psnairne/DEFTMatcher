from deft_matcher.ontology_class import OntologyClass
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)


class ConsoleInterface(UserInterface):
    """
    An interface which uses the console to interact with the user.
    """

    interface: UserInterface

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        return "ConsoleInterface"

    def user_selection(
        self, free_text: str, candidates: list[OntologyClass]
    ) -> OntologyClass | None:
        print("--------------------")
        print(f"{free_text}")
        print("-----CANDIDATES-----")
        for i, candidate in enumerate(candidates):
            print(f"[{i + 1}] {candidate}")
        print("--------------------")
        choice = input("Choose a match: ").strip()
        if choice.lower() == "x":
            return None

        return candidates[int(choice) - 1]
