from deft_matcher.matcher import Matcher
from deft_matcher.retriever import Retriever
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)
from deft_matcher.ontology_class import OntologyClass


class HumanMatcher(Matcher):
    """
    A Homo Sapiens matches the free text to an OntologyClass.
    They may be aided by a list of candidates.
    """

    interface: UserInterface
    candidate_retriever: Retriever

    def __init__(
        self, interface: UserInterface, candidate_retriever: Retriever | None
    ) -> None:
        self.interface = interface
        self.candidate_retriever = candidate_retriever

    @property
    def name(self) -> str:
        return "HumanMatcher"

    def match(self, free_text: str) -> OntologyClass | None:
        if self.candidate_retriever is not None:
            candidates: list[OntologyClass] = self.candidate_retriever.get_matches(
                free_text
            )
        else:
            candidates = []

        user_choice = self.interface.user_selection(free_text, candidates)
        return user_choice
