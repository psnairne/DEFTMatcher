from deft_matcher.ambiguity_resolver import AmbiguityResolver
from deft_matcher.matcher import Matcher


class DecisiveMatcher:

    matcher: Matcher
    ambiguity_resolver: AmbiguityResolver

    def __init__(self, matcher: Matcher, ambiguity_resolver: AmbiguityResolver) -> None:
        self.matcher = matcher
        self.ambiguity_resolver = ambiguity_resolver
