from typing import Optional

from deft_matcher.ambiguity_resolver import AmbiguityResolver


class ChooseFirst(AmbiguityResolver):
    @property
    def name(self) -> str:
        return "ChooseFirst"

    def resolve(self, possible_matches: list[str]) -> Optional[str]:
        return possible_matches[0] if possible_matches else None
