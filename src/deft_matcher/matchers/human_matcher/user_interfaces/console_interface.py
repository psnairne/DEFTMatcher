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
        print(
            "-----FREE TEXT-------------------------------------------------------------------"
        )
        print(f"{free_text}")

        if not candidates:
            print("--------------------")
            print("No candidates found or provided.")
            print("--------------------")
            while True:
                choice = input(
                    "Choose a HPO ID of the form 'HP:1234567' (or 'x' for none): "
                ).strip()

                if choice.lower() == "x":
                    return None
                elif choice.lower().startswith("hp:"):
                    if choice in self._id_to_term_hpo:
                        term = self._id_to_term_hpo[choice]
                        print(f"{term} chosen.")
                        return term
                    else:
                        print(
                            f"Inputted HPO ID '{choice}' was not valid. Please enter a valid HPO ID from release {self.hpo_version}."
                        )
                else:
                    print(
                        "Choice was not valid. Please choose a HPO ID of the form 'HP:1234567', or 'x' for none."
                    )

        if candidates:
            print("-----CANDIDATES-----")
            for i, candidate in enumerate(candidates):
                print(f"[{i + 1}] {candidate}")
            print("--------------------")

            while True:
                choice = input(
                    "Choose a candidate or a HPO ID of the form 'HP:1234567' (or 'x' for none): "
                ).strip()

                if choice.lower() == "x":
                    return None
                elif choice.lower().startswith("hp:"):
                    if choice in self._id_to_term_hpo:
                        term = self._id_to_term_hpo[choice]
                        print(f"{term} chosen.")
                        return term
                    else:
                        print(
                            f"Inputted HPO ID '{choice}' was not valid. Please enter a valid HPO ID from release {self.hpo_version}."
                        )
                elif choice.isdigit():
                    choice_int = int(choice)
                    if choice_int in range(1, len(candidates) + 1):
                        return candidates[int(choice) - 1]
                    else:
                        print(
                            f"Provided integer {choice} was out of range. Please choose a candidate between '1' and '{len(candidates)}'."
                        )
                else:
                    print(
                        f"Choice was not valid. Please choose a candidate between '1' and '{len(candidates)}', a HPO ID of the form 'HP:1234567', or 'x' for none."
                    )

        return None
