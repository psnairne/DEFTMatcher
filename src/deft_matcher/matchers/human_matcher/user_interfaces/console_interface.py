import hpotk
from hpotk import Ontology

from deft_matcher.ontology_class import OntologyClass
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)
from deft_matcher.utils import get_oc


class ConsoleInterface(UserInterface):
    """
    An interface which uses the console to interact with the user.
    """

    interface: UserInterface
    hpo_version: str

    def __init__(self, hpo_version: str) -> None:
        self.hpo_version = hpo_version
        self._hpo = self._initialise_hpo()
        self._id_to_term_hpo = self._initialise_id_to_term_hpo()

    @property
    def name(self) -> str:
        return "ConsoleInterface"

    def _initialise_hpo(self) -> Ontology:
        store = hpotk.configure_ontology_store()
        return store.load_hpo(release=self.hpo_version)

    def _initialise_id_to_term_hpo(self) -> dict[str, OntologyClass]:
        return {term.identifier.value: get_oc(term) for term in self._hpo.terms}

    def user_selection(
        self, free_text: str, candidates: list[OntologyClass]
    ) -> OntologyClass | None:
        self.print_free_text(free_text)
        self.print_candidates(candidates)

        selected_term = None

        while True:
            choice = self.request_input(candidates)

            if choice.lower() == "x":
                break

            if choice.lower().startswith("hp:"):
                if choice in self._id_to_term_hpo:
                    selected_term = self._id_to_term_hpo[choice]
                    break
                else:
                    self.print_invalid_hpo_input(choice)
                    continue

            if choice.isdigit() and candidates:
                choice_int = int(choice)
                if choice_int in range(1, len(candidates) + 1):
                    selected_term = candidates[choice_int - 1]
                    break
                else:
                    self.print_invalid_integer_input(choice, candidates)
                    continue

            self.print_invalid_input(candidates)

        print(f"You chose: {selected_term}.")
        return selected_term

    # -------- OUTPUT STRINGS --------

    @staticmethod
    def print_free_text(free_text: str):
        print(
            "-----FREE TEXT-------------------------------------------------------------------"
        )
        print(f"{free_text}")

    @staticmethod
    def print_candidates(candidates: list[OntologyClass]):
        if candidates:
            print("-----CANDIDATES-----")
            for i, candidate in enumerate(candidates):
                print(f"[{i + 1}] {candidate}")
            print("--------------------")
        else:
            print("--------------------")
            print("No candidates found or provided.")
            print("--------------------")

    def print_invalid_hpo_input(self, choice: str):
        print(
            f"Inputted HPO ID '{choice}' was not valid. Please enter a valid HPO ID from release {self.hpo_version}."
        )

    @staticmethod
    def print_invalid_integer_input(choice: str, candidates: list[OntologyClass]):
        print(
            f"Provided integer {choice} was out of range. Please choose a candidate between '1' and '{len(candidates)}'."
        )

    @staticmethod
    def request_input(candidates: list[OntologyClass]) -> str:
        if candidates:
            choice = input(
                "Choose a candidate or a HPO ID of the form 'HP:1234567' (or 'x' for none): "
            ).strip()
        else:
            choice = input(
                "Choose a HPO ID of the form 'HP:1234567' (or 'x' for none): "
            ).strip()
        return choice

    @staticmethod
    def print_invalid_input(candidates: list[OntologyClass]):
        if candidates:
            print(
                f"Choice was not valid. Please choose a candidate between '1' and '{len(candidates)}', a HPO ID of the form 'HP:1234567', or 'x' for none."
            )
        else:
            print(
                "Choice was not valid. Please choose a HPO ID of the form 'HP:1234567', or 'x' for none."
            )
