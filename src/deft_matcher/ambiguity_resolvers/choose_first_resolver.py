from deft_matcher.ambiguity_resolver import AmbiguityResolver


class ChooseFirstResolver(AmbiguityResolver):
    """
    The simplest ambiguity resolver imaginable.

    If there is a list of possibilities, choose the first.
    """

    @property
    def name(self) -> str:
        return "ChooseFirstResolver"

    def resolve(self, possible_matches: list[str]) -> str | None:
        return possible_matches[0] if possible_matches else None
