from deft_matcher.ambiguity_resolver import AmbiguityResolver
from deft_matcher.matcher import Matcher


class DecisiveMatcher:
    """
    Simply a combination of a Matcher and an AmbiguityResolver.
    Together these can unambiguously match free text to a single string.
    """

    matcher: Matcher
    ambiguity_resolver: AmbiguityResolver

    def __init__(self, matcher: Matcher, ambiguity_resolver: AmbiguityResolver) -> None:
        self.matcher = matcher
        self.ambiguity_resolver = ambiguity_resolver
