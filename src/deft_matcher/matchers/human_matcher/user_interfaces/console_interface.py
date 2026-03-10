from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface

from deft_matcher.utils import validate_file_path_has_version_and_return
from deft_matcher.ontology_class import OntologyClass
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)


class ConsoleInterface(UserInterface):
    """
    An interface which uses the console to interact with the user.
    """

    ontology_prefix: str
    ontology_obo_path: str
    root_term: str
    ontology_version: str
    interface: UserInterface
    _all_term_ids: set[str]
    _id_to_term: dict[str, OntologyClass]
    _label_to_term: dict[str, OntologyClass]

    def __init__(
        self, ontology_prefix: str, ontology_obo_path: str, root_term: str
    ) -> None:
        self.ontology_prefix = ontology_prefix
        self.ontology_obo_path = ontology_obo_path
        self.root_term = root_term
        self.ontology_version = validate_file_path_has_version_and_return(
            self.ontology_obo_path
        )
        self._oak_ontology_str = self._initialise_oak_ontology_str()
        self._ontology = self._initialise_ontology()
        self._all_term_ids = self._initialise_all_term_ids()
        self._id_to_term = self._initialise_id_to_term()
        self._label_to_term = self._initialise_label_to_term()

    @property
    def name(self) -> str:
        return f"ConsoleInterface({self.ontology_prefix.upper()})"

    def _initialise_oak_ontology_str(self) -> str:
        return "simpleobo:" + self.ontology_obo_path

    def _initialise_ontology(self) -> OboGraphInterface:
        return get_adapter(self._oak_ontology_str)

    def _initialise_all_term_ids(self) -> set[str]:
        return set(self._ontology.descendants(self.root_term, predicates=[IS_A]))

    def _initialise_id_to_term(self) -> dict[str, OntologyClass]:
        id_to_term: dict[str, OntologyClass] = dict()
        for term_id in self._all_term_ids:
            id_to_term[term_id] = OntologyClass.from_term_id(term_id, self._ontology)
        return id_to_term

    def _initialise_label_to_term(self) -> dict[str, OntologyClass]:
        label_to_term: dict[str, OntologyClass] = dict()
        for term_id in self._all_term_ids:
            label: str = self._ontology.label(term_id)
            label_to_term[label.lower()] = OntologyClass.from_term_id(
                term_id, self._ontology
            )
        return label_to_term

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

            if choice.lower().startswith(f"{self.ontology_prefix.lower()}:"):
                if choice in self._id_to_term:
                    selected_term = self._id_to_term[choice]
                    break
                else:
                    self.print_invalid_id_input(choice)
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

        seen_ancestors: set[OntologyClass] = set(candidates)

        candidate_ancestor_encoding: dict[str, OntologyClass] = {}
        for i, candidate in enumerate(candidates, start=1):
            candidate_ancestor_encoding[str(i)] = candidate
            j: int = 0  # counts how many ancestors for this candidate we are displaying

            ancestors: list[str] = self.get_ordered_ancestors(candidate)

            for ancestor in ancestors:
                if not ancestor.startswith(self.ontology_prefix.upper()):
                    continue

                if ancestor == self.root_term:
                    continue

                ancestor_oc = OntologyClass.from_term_id(ancestor, self._ontology)
                if ancestor_oc in seen_ancestors:
                    continue
                else:
                    j += 1
                    candidate_ancestor_encoding[f"{i}.{j}"] = ancestor_oc
                    seen_ancestors.add(ancestor_oc)

        return candidate_ancestor_encoding

    def get_ordered_ancestors(self, candidate: OntologyClass) -> list[str]:
        """
        Returns ancestors of the candidate, ordered from most specific
        (closest to start) to most general (furthest from start).
        """

        visited: set[str] = set()
        queue: list[str] = [candidate.curie_id]
        ancestor_distance: dict[str, int] = {candidate.curie_id: 0}

        index = 0
        while index < len(queue):
            child = queue[index]
            for parent in self._ontology.hierarchical_parents(child):
                if parent not in visited and parent in self._all_term_ids:
                    visited.add(parent)
                    ancestor_distance[parent] = ancestor_distance.get(child) + 1
                    queue.append(parent)
            index += 1

        ancestors_sorted = sorted(
            ancestor_distance.keys(), key=lambda a: ancestor_distance[a]
        )
        return ancestors_sorted

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

    def print_invalid_id_input(self, choice: str):
        print(
            f"Inputted ID '{choice}' was not valid. Please enter a valid ID from ontology {self.ontology_prefix.upper()} release {self.ontology_version} with root {self._ontology.label(self.root_term)}."
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

    def request_input(self, candidates: list[OntologyClass]) -> str:
        if candidates:
            choice = input(
                f"Choose a candidate or an ontology ID of the form '{self.ontology_prefix.upper()}:1234567' (or 'x' for none): "
            ).strip()
        else:
            choice = input(
                "Choose an ontology ID of the form 'PREFIX:1234567' (or 'x' for none): "
            ).strip()
        return choice

    def print_invalid_input(self, candidates: list[OntologyClass]):
        if candidates:
            print(
                f"Choice was not valid. Please choose a candidate, an ontology ID of the form '{self.ontology_prefix.upper()}:1234567', or 'x' for none."
            )
        else:
            print(
                f"Choice was not valid. Please choose an ontology ID of the form '{self.ontology_prefix.upper()}:1234567', or 'x' for none."
            )
