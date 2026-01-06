import random

from tqdm import tqdm

from deft_matcher.ambiguity_resolver import AmbiguityResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.matcher import Matcher
from pathlib import Path
from datetime import datetime
import logging
from logging import Logger


class DeftMatcher:
    """
    Solves all your free text matching problems.

    Just provide your free texts, and your ordered list of DecisiveMatchers.

    The .next() function is your friend.
    """

    decisive_matchers: list[DecisiveMatcher]
    next_index: int
    next_matcher: Matcher | None
    next_resolver: AmbiguityResolver | None
    matched: dict[str, str]
    unmatched: set[str]
    logger: Logger
    data_name: str

    def __init__(
        self,
        decisive_matchers: list[DecisiveMatcher],
        free_texts: set[str],
        data_name: str,
    ) -> None:
        self.decisive_matchers = decisive_matchers
        self.next_index = 0
        self.next_matcher = self.get_next_matcher_from_next_index()
        self.next_resolver = self.get_next_resolver_from_next_index()
        self.matched = {}
        self.unmatched = free_texts
        self.logger = self.initialise_logger()
        self.data_name = data_name

        self.logger.info(self.startup_log_str())

    def run(self):
        """
        Applies all DecisiveMatchers in order.
        """

        for dm_no in range(len(self.decisive_matchers)):
            self.next()

    def next(self):
        """
        Applies the next DecisiveMatcher to the remaining unmatched strings.
        """
        if self.no_more_matchers_or_resolvers():
            self.logger.info(self.no_more_matchers_or_resolvers_str())
            return

        matcher: Matcher = self.next_matcher
        resolver: AmbiguityResolver = self.next_resolver

        self.log_new_matcher_and_resolver(
            matcher_name=matcher.name, resolver_name=resolver.name
        )

        self.match(unmatched=self.unmatched, matcher=matcher, resolver=resolver)

    def match(self, unmatched: set[str], matcher: Matcher, resolver: AmbiguityResolver):
        solved: list[str] = []

        for free_text in unmatched:
            matches = matcher.get_matches(free_text)
            resolution = resolver.resolve(matches)

            if resolution is not None:
                self.matched[free_text] = resolution
                solved.append(free_text)
                self.logger.info(f"{free_text} was matched to {resolution}!")
            else:
                self.logger.info(f"{free_text} had no resolution.")

        self.unmatched -= set(solved)
        self.next_index += 1
        self.next_matcher = self.get_next_matcher_from_next_index()
        self.next_resolver = self.get_next_resolver_from_next_index()

        self.log_match_info(
            matcher_name=matcher.name, resolver_name=resolver.name, solved=solved
        )

    def get_next_matcher_from_next_index(self) -> Matcher | None:
        if self.next_index <= len(self.decisive_matchers) - 1:
            return self.decisive_matchers[self.next_index].matcher
        else:
            return None

    def get_next_resolver_from_next_index(self) -> AmbiguityResolver | None:
        if self.next_index <= len(self.decisive_matchers) - 1:
            return self.decisive_matchers[self.next_index].ambiguity_resolver
        else:
            return None

    def no_more_matchers_or_resolvers(self) -> bool:
        if self.next_matcher is None or self.next_resolver is None:
            return True
        else:
            return False

    def update_attributes(self, solved_free_texts: list[str]):
        self.unmatched -= set(solved_free_texts)
        self.next_index += 1
        self.next_matcher = self.get_next_matcher_from_next_index()
        self.next_resolver = self.get_next_resolver_from_next_index()

    # ---------------- LOGGING METHODS ----------------

    @staticmethod
    def initialise_logger() -> Logger:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        log_file = log_dir / f"{timestamp}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file)],
            force=True,
        )

        logger = logging.getLogger()

        return logger

    def startup_log_str(self):
        header_str = f"Applying the DEFTMatcher pipeline to {self.data_name} with matchers and resolvers:\n"
        matcher_resolver_str = "\n".join(
            f"  - {dm.matcher.name} and {dm.ambiguity_resolver.name}"
            for dm in self.decisive_matchers
        )
        return header_str + matcher_resolver_str

    def log_new_matcher_and_resolver(self, matcher_name: str, resolver_name: str):
        self.logger.info(
            f"Applying matcher {matcher_name} and resolver {resolver_name} to {len(self.unmatched)} unmatched strings."
        )

    def log_match_info(self, matcher_name: str, resolver_name: str, solved: list[str]):
        """Logs our progress after applying a matcher and resolver."""

        log_parts = [
            self.header_log_str(matcher_name, resolver_name),
            self.solved_log_str(solved, 3),
            self.unsolved_log_str(3),
            self.footer_log_str(),
        ]

        self.logger.info("\n".join(log_parts))

    @staticmethod
    def header_log_str(matcher_name: str, resolver_name: str) -> str:
        return f"Matcher {matcher_name} and resolver {resolver_name} were successfully applied."

    def solved_log_str(self, solved: list[str], max_examples: int) -> str:
        num_solved = len(solved)
        num_examples = min(max_examples, num_solved)

        if num_solved == 0:
            return "No strings were matched."
        elif num_solved == 1:
            solved_text = solved[0]
            return f"Only 1 string was matched: {self.example_match_str(solved_text, self.matched[solved_text])}."
        else:
            examples = [
                self.example_match_str(text, self.matched[text])
                for text in solved[:num_examples]
            ]
            examples_str = "\n".join(f"  - {ex}" for ex in examples)

            if num_solved == num_examples:
                return f"{num_solved} strings were matched, namely:\n{examples_str}"
            else:
                return (
                    f"{num_solved} strings were matched, for example:\n{examples_str}"
                )

    def unsolved_log_str(self, max_examples: int) -> str:
        unsolved = list(self.unmatched)
        random.shuffle(unsolved)

        num_unsolved = len(unsolved)
        num_examples = min(max_examples, num_unsolved)

        if num_unsolved == 0:
            return "All strings have been matched!"
        elif num_unsolved == 1:
            unsolved_text = unsolved[0]
            return f"There remains just 1 unmatched string: '{unsolved_text}'."
        else:
            examples = unsolved[:num_examples]
            examples_str = "\n".join(f"  - '{ex}'" for ex in examples)

            if num_unsolved == num_examples:
                return f"There remain {num_unsolved} unmatched strings, namely:\n{examples_str}"
            else:
                return f"There remain {num_unsolved} unmatched strings, for example:\n{examples_str}"

    def footer_log_str(self) -> str:
        if self.no_more_matchers_or_resolvers():
            return self.no_more_matchers_or_resolvers_str()
        else:
            return f"The next matcher is {self.next_matcher.name} and the next resolver is {self.next_resolver.name}."

    @staticmethod
    def example_match_str(text: str, text_match: str) -> str:
        return f"'{text}' → '{text_match}'"

    @staticmethod
    def no_more_matchers_or_resolvers_str() -> str:
        return "There are no more matchers or resolvers!"
