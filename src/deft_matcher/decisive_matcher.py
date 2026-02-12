from deft_matcher.ambiguity_resolver import AmbiguityResolver
from deft_matcher.matcher import Matcher


class DecisiveMatcher:
    """
    Simply a combination of a Matcher and an AmbiguityResolver.
    Together these can unambiguously match free text to a single OntologyClass.
    """

    matcher: Matcher
    ambiguity_resolver: AmbiguityResolver
    name: str

    def __init__(self, matcher: Matcher, ambiguity_resolver: AmbiguityResolver) -> None:
        self.matcher = matcher
        self.ambiguity_resolver = ambiguity_resolver
        self.name = self._initialise_name()

    def _initialise_name(self) -> str:
        name = self.matcher.name + "+" + self.ambiguity_resolver.name
        return name
