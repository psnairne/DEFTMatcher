from deft_matcher.resolver import Resolver
from deft_matcher.ontology_class import OntologyClass


class ChooseFirstResolver(Resolver):
    """
    The simplest resolver imaginable.

    If there is a list of possibilities, choose the first.
    """

    @property
    def name(self) -> str:
        return "ChooseFirstResolver"

    def resolve(self, possible_matches: list[OntologyClass]) -> OntologyClass | None:
        return possible_matches[0] if possible_matches else None
