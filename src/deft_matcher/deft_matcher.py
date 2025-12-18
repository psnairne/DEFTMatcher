import random
from typing import Optional
from deft_matcher.ambiguity_resolver import AmbiguityResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.matcher import Matcher


class FreeTextNormaliser:
    decisive_matchers: list[DecisiveMatcher]
    next_index: int
    next_matcher: Matcher | None
    next_resolver: AmbiguityResolver | None
    matched: dict[str, str]
    unmatched: set[str]

    def __init__(
        self, decisive_matchers: list[DecisiveMatcher], free_texts: set[str]
    ) -> None:
        self.decisive_matchers = decisive_matchers
        self.next_index = 0
        self.next_matcher = self.get_next_matcher_from_next_index()
        self.next_resolver = self.get_next_resolver_from_next_index()
        self.matched = {}
        self.unmatched = free_texts

    def get_next_matcher_from_next_index(self) -> Optional[Matcher]:
        if self.next_index <= len(self.decisive_matchers) - 1:
            return self.decisive_matchers[self.next_index].matcher
        else:
            return None

    def get_next_resolver_from_next_index(self) -> Optional[AmbiguityResolver]:
        if self.next_index <= len(self.decisive_matchers) - 1:
            return self.decisive_matchers[self.next_index].ambiguity_resolver
        else:
            return None

    def no_more_matchers_or_resolvers(self) -> bool:
        if self.next_matcher is None or self.next_resolver is None:
            return True
        else:
            return False

    @staticmethod
    def no_more_matchers_or_resolvers_alert():
        print("There are no more matchers or resolvers!")

    def next(self):
        if self.no_more_matchers_or_resolvers():
            self.no_more_matchers_or_resolvers_alert()
            return

        matcher: Matcher = self.next_matcher
        resolver: AmbiguityResolver = self.next_resolver

        print(
            f"\n\nApplying matcher {matcher.name} and resolver {resolver.name} to {len(self.unmatched)} unmatched strings."
        )

        solved_free_texts: list[str] = []

        for free_text in self.unmatched:
            possible_matches = matcher.get_matches(free_text)
            possible_resolution = resolver.resolve(possible_matches)

            if possible_resolution is not None:
                self.matched[free_text] = possible_resolution
                solved_free_texts.append(free_text)

        self.unmatched -= set(solved_free_texts)
        self.next_index += 1
        self.next_matcher = self.get_next_matcher_from_next_index()
        self.next_resolver = self.get_next_resolver_from_next_index()

        print(
            f"Matcher {matcher.name} and resolver {resolver.name} were successfully applied."
        )

        self.print_helpful_info_on_matching(solved_free_texts)

        if self.no_more_matchers_or_resolvers():
            self.no_more_matchers_or_resolvers_alert()
        else:
            print(
                f"The next matcher is {self.next_matcher.name} and the next resolver is {self.next_resolver.name}."
            )

    def print_helpful_info_on_matching(self, solved_free_texts: list[str]):
        # TODO this can be improved so that the amount we show is adjustable. And you probably want helpful infos split between more lines.

        # PRINT INFO ON WHAT HAS BEEN MATCHED

        if len(solved_free_texts) > 2:
            first_example = solved_free_texts[0]
            first_example_match = self.matched[first_example]
            second_example = solved_free_texts[1]
            second_example_match = self.matched[second_example]

            print(
                f"{len(solved_free_texts)} strings were matched, for example, '{first_example}' was matched to {first_example_match} and '{second_example}' was matched to {second_example_match}."
            )
        elif len(solved_free_texts) == 2:
            first_example = solved_free_texts[0]
            first_example_match = self.matched[first_example]
            second_example = solved_free_texts[1]
            second_example_match = self.matched[second_example]

            print(
                f"{len(solved_free_texts)} strings were matched, namely '{first_example}' was matched to {first_example_match} and '{second_example}' was matched to {second_example_match}."
            )
        elif len(solved_free_texts) == 1:
            example = solved_free_texts[0]
            example_match = self.matched[example]
            print(
                f"Only 1 string was matched, namely '{example}' was matched to {example_match}."
            )
        elif len(solved_free_texts) == 0:
            print("No strings were matched.")

        # PRINT INFO ON WHAT STILL NEEDS TO BE MATCHED

        unmatched = list(self.unmatched)
        random.shuffle(unmatched)

        if len(unmatched) > 2:
            first_example = unmatched[0]
            second_example = unmatched[1]
            print(
                f"There remain {len(self.unmatched)} unmatched strings. For example '{first_example}' and '{second_example}'."
            )
        elif len(unmatched) == 2:
            first_example = unmatched[0]
            second_example = unmatched[1]
            print(
                f"There remain {len(self.unmatched)} unmatched strings. Namely '{first_example}' and '{second_example}'."
            )
        elif len(unmatched) == 1:
            example = unmatched[0]
            print(f"There remains just 1 unmatched string. Namely '{example}'.")
        elif len(unmatched) == 0:
            print("All strings have been matched!")
