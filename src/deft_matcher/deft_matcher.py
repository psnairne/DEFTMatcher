import json
import random
from dataclasses import dataclass, asdict
from typing import Any
from uuid import uuid4

import pandas as pd
from pandas import DataFrame

from deft_matcher.ambiguity_resolver import AmbiguityResolver
from deft_matcher.decisive_matcher import DecisiveMatcher
from deft_matcher.matcher import Matcher
from pathlib import Path
from datetime import datetime
import logging
from logging import Logger

from deft_matcher.ontology_class import OntologyClass


@dataclass
class DeftMatcherConfig:
    """
    Holds the configuration for a DeftMatcher pipeline.
    """

    decisive_matchers: list[DecisiveMatcher]


@dataclass
class DeftMatcherData:
    """
    Holds the data input for a DeftMatcher pipeline.
    """

    free_texts: list[str]
    data_name: str


@dataclass(frozen=True)
class MatchData:
    """
    Holds info on a match made by DEFTMatcher.
    """

    match: OntologyClass
    matcher_name: str
    resolver_name: str


@dataclass(frozen=True)
class MetaDataStatistics:
    """
    Holds serialisable statistics on the results of a DeftMatcher pipeline.
    """

    number_of_free_texts: int
    number_of_unique_free_texts: int
    number_of_free_texts_matched: int
    number_of_unique_free_texts_matched: int
    number_of_free_texts_unmatched: int
    number_of_unique_free_texts_unmatched: int
    unique_free_texts_matched_by_decisive_matcher: dict[str, int]


@dataclass(frozen=True)
class MetaData:
    """
    Holds serialisable info on the set-up and results of a DeftMatcher pipeline.
    """

    data_name: str
    time_started: str
    time_created: str
    decisive_matchers: list[tuple[str, str]]
    matching_uuid: str
    statistics: MetaDataStatistics
    unique_unmatched_free_texts: list[str]


class DeftMatcher:
    """
    Solves all your free text matching problems.

    Just provide your free texts, and your ordered list of DecisiveMatchers.

    The .next() and the .run() functions are your friends.
    """

    time_started: str
    decisive_matchers: list[DecisiveMatcher]
    next_index: int
    next_matcher: Matcher | None
    next_resolver: AmbiguityResolver | None
    free_texts: list[str]
    matchings: dict[str, MatchData]
    unmatched: set[str]
    logger: Logger
    data_name: str

    def __init__(self, config: DeftMatcherConfig, data: DeftMatcherData) -> None:
        self.time_started = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.decisive_matchers = config.decisive_matchers
        self.next_index = 0
        self.next_matcher = self.get_next_matcher_from_next_index()
        self.next_resolver = self.get_next_resolver_from_next_index()
        self.free_texts = data.free_texts
        self.unmatched = set(data.free_texts)
        self.matchings = {}
        self.logger = self.initialise_logger()
        self.data_name = data.data_name
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
        matcher_name = matcher.name
        resolver_name = resolver.name

        solved: list[str] = []

        for free_text in unmatched:
            matches: list[OntologyClass] = matcher.get_matches(free_text)
            resolution: OntologyClass | None = resolver.resolve(matches)

            if resolution is not None:
                self.matchings[free_text] = MatchData(
                    resolution, matcher_name, resolver_name
                )
                solved.append(free_text)
                self.logger.info(f"{free_text} was matched to {resolution}.")
            else:
                self.logger.info(f"{free_text} had no resolution.")

        self.update_attributes(solved_free_texts=solved)

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

    # ---------------- LOADING A STATE ----------------

    @classmethod
    def load_state_from_files(
        cls,
        matching_file_path: str,
        metadata_file_path: str,
        decisive_matchers: list[DecisiveMatcher],
    ) -> "DeftMatcher":
        """
        Will create a new DeftMatcher object based on the data provided in the matching and metadata_file_path.

        So you can continue where you left off, or make edits.
        """

        obj: DeftMatcher = cls.__new__(cls)

        obj.time_started = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        obj.decisive_matchers = decisive_matchers
        obj.next_index = 0
        obj.next_matcher = obj.get_next_matcher_from_next_index()
        obj.next_resolver = obj.get_next_resolver_from_next_index()
        obj.logger = obj.initialise_logger()

        # load matchings and free_texts
        cls.load_matchings_from_file(obj, matching_file_path)

        # load unmatched and data_name
        cls.load_unmatched_from_file(obj, metadata_file_path)

        obj.logger.info(
            obj.startup_from_file_log_str(matching_file_path, metadata_file_path)
        )
        obj.logger.info(obj.startup_log_str())

        return obj

    @staticmethod
    def load_matchings_from_file(obj: "DeftMatcher", matching_file_path: str) -> None:
        matching_df: DataFrame = pd.read_csv(matching_file_path)
        matching_df.itertuples()

        matchings: dict[str, MatchData] = {}

        for row in matching_df.itertuples(index=False, name="Row"):
            free_text: str = getattr(row, "FREE_TEXT")
            curie_id: str = getattr(row, "CURIE_ID")
            label: str = getattr(row, "LABEL")
            matcher: str = getattr(row, "MATCHER")
            resolver: str = getattr(row, "RESOLVER")
            match_data = MatchData(
                OntologyClass(curie_id, label),
                matcher_name=matcher,
                resolver_name=resolver,
            )
            matchings[free_text] = match_data

        obj.matchings = matchings
        obj.free_texts = list(matchings.keys())

    @staticmethod
    def load_unmatched_from_file(obj: "DeftMatcher", metadata_file_path: str) -> None:
        with open(metadata_file_path, "r", encoding="utf-8") as f:
            metadata: dict[str, Any] = json.load(f)

        obj.data_name = metadata["data_name"]
        obj.unmatched = set(metadata["unique_unmatched_free_texts"])

    # ---------------- OUTPUTTING RESULTS ----------------

    def output_results(self, output_dir: Path):
        uuid: str = str(uuid4())

        results_dir: Path = (
            output_dir / f"deft_matcher_results_{uuid}_{self.time_started}"
        )
        results_dir.mkdir(parents=True, exist_ok=False)

        self.logger.info(f"Outputting DEFTMatcher results to folder {results_dir}.")

        results_df: DataFrame = self.create_results_df()
        metadata: MetaData = self.create_metadata(uuid)

        matchings_path: Path = results_dir / "matchings.csv"
        metadata_path: Path = results_dir / "metadata.json"

        results_df.to_csv(matchings_path, index=False)

        with metadata_path.open("w", encoding="utf-8") as f:
            json.dump(asdict(metadata), f, indent=2)

        self.logger.info(
            f"DEFTMatcher results successfully outputted to folder {results_dir}."
        )

    def create_results_df(self) -> DataFrame:
        df: DataFrame = pd.DataFrame(
            [
                {
                    "FREE_TEXT": free_text,
                    "CURIE_ID": data.match.curie_id,
                    "LABEL": data.match.label,
                    "MATCHER": data.matcher_name,
                    "RESOLVER": data.resolver_name,
                }
                for free_text, data in self.matchings.items()
            ]
        )
        return df

    def create_metadata(self, matching_uuid: str) -> MetaData:
        decisive_matchers_applied: list[DecisiveMatcher] = self.decisive_matchers[
            0 : self.next_index
        ]

        statistics = MetaDataStatistics(
            number_of_free_texts=len(self.free_texts),
            number_of_unique_free_texts=len(set(self.free_texts)),
            number_of_free_texts_matched=sum(
                1 for item in self.free_texts if item in self.matchings
            ),
            number_of_unique_free_texts_matched=len(self.matchings),
            number_of_free_texts_unmatched=sum(
                1 for item in self.free_texts if item not in self.matchings
            ),
            number_of_unique_free_texts_unmatched=len(self.unmatched),
            unique_free_texts_matched_by_decisive_matcher=self.get_unique_free_texts_by_decisive_matcher(),
        )

        metadata = MetaData(
            data_name=self.data_name,
            time_started=self.time_started,
            time_created=datetime.now().strftime("%d-%m-%Y_%H-%M-%S"),
            decisive_matchers=[
                (dm.matcher.name, dm.ambiguity_resolver.name)
                for dm in decisive_matchers_applied
            ],
            matching_uuid=matching_uuid,
            statistics=statistics,
            unique_unmatched_free_texts=list(self.unmatched),
        )

        return metadata

    def get_unique_free_texts_by_decisive_matcher(self) -> dict[str, int]:
        count_dict: dict[str, int] = {}

        for match_data in self.matchings.values():
            decisive_matcher_name = (
                match_data.matcher_name + "+" + match_data.resolver_name
            )
            count_dict[decisive_matcher_name] = (
                count_dict.get(decisive_matcher_name, 0) + 1
            )

        return count_dict

    # ---------------- LOGGING METHODS ----------------

    def initialise_logger(self) -> Logger:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        timestamp = self.time_started
        log_file = log_dir / f"{timestamp}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file)],
            force=True,
        )

        logger = logging.getLogger()

        return logger

    def startup_log_str(self) -> str:
        header_str = f"Applying the DEFTMatcher pipeline to {self.data_name} with matchers and resolvers:\n"
        matcher_resolver_str = "\n".join(
            f"  - {dm.matcher.name} and {dm.ambiguity_resolver.name}"
            for dm in self.decisive_matchers
        )
        return header_str + matcher_resolver_str

    @staticmethod
    def startup_from_file_log_str(
        matching_file_path: str, metadata_file_path: str
    ) -> str:
        return f"DeftMatcher object loaded from {matching_file_path} and {metadata_file_path}"

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
            return f"Only 1 string was matched: {self.example_match_str(solved_text, self.matchings[solved_text].match.label)}."
        else:
            examples = [
                self.example_match_str(text, self.matchings[text].match.label)
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
