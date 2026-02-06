import hpotk
from hpotk import Ontology

from deft_matcher.ontology_class import OntologyClass
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)


class ConsoleInterfaceHpo(UserInterface):
    """
    An interface which uses the console to interact with the user.
    Currently this is only designed to work with HPO.
    """

    interface: UserInterface
    hpo_version: str
    _id_to_term_hpo: dict[str, OntologyClass]
    _label_to_term_hpo: dict[str, OntologyClass]

    def __init__(self, hpo_version: str) -> None:
        self.hpo_version = hpo_version
        self._hpo = self._initialise_hpo()
        self._id_to_term_hpo = self._initialise_id_to_term_hpo()
        self._label_to_term_hpo = self._initialise_label_to_term_hpo()

    @property
    def name(self) -> str:
        return "ConsoleInterfaceHpo"

    def _initialise_hpo(self) -> Ontology:
        store = hpotk.configure_ontology_store()
        return store.load_hpo(release=self.hpo_version)

    def _initialise_id_to_term_hpo(self) -> dict[str, OntologyClass]:
        return {
            term.identifier.value: OntologyClass.from_minimal_term(term)
            for term in self._hpo.terms
        }

    def _initialise_label_to_term_hpo(self) -> dict[str, OntologyClass]:
        return {
            term.name: OntologyClass.from_minimal_term(term) for term in self._hpo.terms
        }

    def user_selection(
        self, free_text: str, candidates: list[OntologyClass]
    ) -> OntologyClass | None:
        self.print_free_text(free_text)
        ca_dict: dict[str, OntologyClass] = self.get_candidate_ancestor_encoding(
            candidates
        )
        self.print_candidates_and_ancestors(ca_dict)

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

            if self.is_candidate_input(choice) and candidates:
                if choice in ca_dict:
                    selected_term = ca_dict[choice]
                    break
                else:
                    self.print_invalid_numeric_input(choice, ca_dict)
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

    def get_candidate_ancestor_encoding(
        self, candidates: list[OntologyClass]
    ) -> dict[str, OntologyClass]:
        if not candidates:
            return {}

        ancestors_to_ignore: set[OntologyClass] = {
            self._label_to_term_hpo["Phenotypic abnormality"],
            self._label_to_term_hpo["All"],
        }
        seen_ancestors: set[OntologyClass] = set()
        candidate_ancestor_encoding: dict[str, OntologyClass] = {}
        for i, candidate in enumerate(candidates, start=1):
            candidate_ancestor_encoding[str(i)] = candidate
            j: int = 0  # counts how many ancestors for this candidate we are displaying

            for ancestor in self._hpo.graph.get_ancestors(candidate.curie_id):
                ancestor_oc = OntologyClass.from_minimal_term(
                    self._hpo.get_term(ancestor)
                )
                if ancestor_oc in seen_ancestors:
                    continue
                if ancestor_oc in ancestors_to_ignore:
                    continue
                else:
                    j += 1
                    candidate_ancestor_encoding[f"{i}.{j}"] = ancestor_oc
                    seen_ancestors.add(ancestor_oc)

        return candidate_ancestor_encoding

    @staticmethod
    def print_candidates_and_ancestors(ca_dict: dict[str, OntologyClass]):
        if not ca_dict:
            print(
                "---------------------------------------------------------------------------------"
            )
            print("No candidates found or provided.")
            print(
                "---------------------------------------------------------------------------------"
            )
        else:
            print(
                "-----CANDIDATES------------------------------------------------------------------"
            )

            candidate_keys = sorted(
                [k for k in ca_dict.keys() if "." not in k], key=int
            )

            for candidate_key in candidate_keys:
                candidate = ca_dict[candidate_key]
                print(f"{candidate_key}: {candidate.label} ({candidate.curie_id})")

                ancestor_keys = sorted(
                    [k for k in ca_dict.keys() if k.startswith(f"{candidate_key}.")],
                    key=lambda x: int(x.split(".")[1]),
                )

                for ancestor_key in ancestor_keys:
                    ancestor = ca_dict[ancestor_key]
                    space = "    "
                    print(
                        f"{space}{ancestor_key}: {ancestor.label} ({ancestor.curie_id})"
                    )

            print(
                "---------------------------------------------------------------------------------"
            )

    def print_invalid_hpo_input(self, choice: str):
        print(
            f"Inputted HPO ID '{choice}' was not valid. Please enter a valid HPO ID from release {self.hpo_version}."
        )

    @staticmethod
    def is_candidate_input(choice: str) -> bool:
        parts = choice.split(".")

        if len(parts) == 1 and parts[0].isdigit():
            return True

        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return True

        return False

    @staticmethod
    def print_invalid_numeric_input(choice: str, ca_dict: dict[str, OntologyClass]):
        options_str: str = ", ".join(ca_dict.keys())
        print(
            f"Candidate selection {choice} was invalid. Please choose one of the options: {options_str}."
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
                "Choice was not valid. Please choose a candidate, a HPO ID of the form 'HP:1234567', or 'x' for none."
            )
        else:
            print(
                "Choice was not valid. Please choose a HPO ID of the form 'HP:1234567', or 'x' for none."
            )
