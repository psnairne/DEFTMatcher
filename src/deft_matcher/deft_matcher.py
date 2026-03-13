import json
import random
from dataclasses import dataclass, asdict
from typing import Any
from uuid import uuid4

import pandas as pd
from pandas import DataFrame

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

    matchers: list[Matcher]


@dataclass
class DeftMatcherData:
    """
    Holds the data input for a DeftMatcher pipeline.
    """

    free_texts: list[str]
    data_name: str

    def __post_init__(self):
        self.free_texts = [str(v) for v in self.free_texts if not pd.isna(v)]


@dataclass(frozen=True)
class MatchData:
    """
    Holds info on a match made by DEFTMatcher.
    """

    match: OntologyClass
    matcher_name: str


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
    unique_free_texts_matched_by_matcher: dict[str, int]


@dataclass(frozen=True)
class MetaData:
    """
    Holds serialisable info on the set-up and results of a DeftMatcher pipeline.
    """

    data_name: str
    time_started: str
    time_created: str
    matchers: list[str]
    matching_uuid: str
    statistics: MetaDataStatistics
    unique_unmatched_free_texts: list[str]


class DeftMatcher:
    """
    Solves all your free text matching problems.

    Just provide your free texts, and your ordered list of Matchers.

    The .next() and the .run() functions are your friends.
    """

    time_started: str
    matchers: list[Matcher]
    next_index: int
    next_matcher: Matcher | None
    free_texts: list[str]
    matchings: dict[str, MatchData]
    unmatched: set[str]
    uuid: str
    logger: Logger
    data_name: str

    def __init__(self, data: DeftMatcherData, config: DeftMatcherConfig) -> None:
        self.time_started = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.matchers = config.matchers
        self.next_index = 0
        self.next_matcher = self.get_next_matcher_from_next_index()
        self.free_texts = data.free_texts
        self.unmatched = set(data.free_texts)
        self.matchings = {}
        self.uuid = str(uuid4())
        self.logger = self.initialise_logger()
        self.data_name = data.data_name
        self.logger.info(self.startup_log_str())

    def run(self):
        """
        Applies all Matchers in order.
        """

        for matcher_index in range(len(self.matchers)):
            self.next()

    def next(self):
        """
        Applies the next Matcher to the remaining unmatched strings.
        """
        if self.no_more_matchers():
            self.logger.info(self.no_more_matchers_str())
            return

        matcher: Matcher = self.next_matcher

        self.log_new_matcher(matcher_name=matcher.name)

        self.run_matcher(matcher=matcher)

    def run_matcher(self, matcher: Matcher):
        matcher_name = matcher.name

        solved: list[str] = []

        for free_text in self.unmatched:
            possible_match: OntologyClass | None = matcher.match(free_text)

            if possible_match is not None:
                self.matchings[free_text] = MatchData(possible_match, matcher_name)
                solved.append(free_text)
                self.logger.info(f"{free_text} was matched to {possible_match}.")
            else:
                self.logger.info(f"{free_text} had no resolution.")

        self.update_attributes(solved_free_texts=solved)

        self.log_match_info(matcher_name=matcher.name, solved=solved)

    def get_next_matcher_from_next_index(self) -> Matcher | None:
        if self.next_index <= len(self.matchers) - 1:
            return self.matchers[self.next_index]
        else:
            return None

    def no_more_matchers(self) -> bool:
        return self.next_matcher is None

    def update_attributes(self, solved_free_texts: list[str]):
        self.unmatched -= set(solved_free_texts)
        self.next_index += 1
        self.next_matcher = self.get_next_matcher_from_next_index()

    # ---------------- LOADING A STATE ----------------

    @classmethod
    def load_state_from_files(
        cls, matching_file_path: str, metadata_file_path: str, matchers: list[Matcher]
    ) -> "DeftMatcher":
        """
        Will create a new DeftMatcher object based on the data provided in the matching and metadata_file_path.

        So you can continue where you left off, or make edits.
        """

        obj: DeftMatcher = cls.__new__(cls)

        obj.time_started = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        obj.matchers = matchers
        obj.next_index = 0
        obj.uuid = str(uuid4())
        obj.next_matcher = obj.get_next_matcher_from_next_index()
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
            match_data = MatchData(OntologyClass(curie_id, label), matcher_name=matcher)
            matchings[free_text] = match_data

        obj.matchings = matchings
        obj.free_texts = list(matchings.keys())

    @staticmethod
    def load_unmatched_from_file(obj: "DeftMatcher", metadata_file_path: str) -> None:
        with open(metadata_file_path, "r", encoding="utf-8") as f:
            metadata: dict[str, Any] = json.load(f)

        obj.data_name = metadata["data_name"]
        obj.unmatched = set(metadata["unique_unmatched_free_texts"])

    # ---------------- EDITING A STATE -------------------

    def rematch(self, free_text: str, replacement_match: OntologyClass) -> None:
        """
        This is used to alter a single matching.
        """

        replacement_match_data: MatchData = MatchData(
            match=replacement_match, matcher_name="HumanEditor"
        )

        if free_text in self.matchings:
            self.matchings[free_text] = replacement_match_data
        else:
            raise KeyError(f"{free_text} was not found among the matchings.")

    def bulk_rematch(self, replacement_matchings: dict[str, OntologyClass]):
        """
        This is used to alter several matchings.
        """

        invalid_keys: list[str] = [
            free_text
            for free_text in replacement_matchings
            if free_text not in self.matchings
        ]

        if invalid_keys:
            raise KeyError(
                f"The following free texts were not found among the matchings: {invalid_keys}."
            )

        for free_text, replacement_match in replacement_matchings.items():
            self.rematch(free_text, replacement_match)

    def unmatch(self, free_text: str) -> None:
        """
        Unmatch a single matching.
        """

        if free_text in self.matchings:
            del self.matchings[free_text]
            self.unmatched.add(free_text)
        else:
            raise KeyError(f"{free_text} was not found among the matchings.")

    def bulk_unmatch(self, free_texts: list[str]) -> None:
        invalid_keys: list[str] = [
            free_text for free_text in free_texts if free_text not in self.matchings
        ]

        if invalid_keys:
            raise KeyError(
                f"The following free texts were not found among the matchings: {invalid_keys}."
            )

        for free_text in free_texts:
            self.unmatch(free_text)

    def match(self, free_text: str, match: OntologyClass):
        """
        Create a single new match.
        """

        new_match_data: MatchData = MatchData(match=match, matcher_name="HumanEditor")

        if free_text in self.unmatched:
            self.matchings[free_text] = new_match_data
            self.unmatched.remove(free_text)
        else:
            raise KeyError(f"{free_text} was not found among the unmatched strings.")

    def bulk_match(self, matchings: dict[str, OntologyClass]):
        """
        Create a several new matches.
        """

        invalid_keys: list[str] = [
            free_text for free_text in matchings if free_text not in self.unmatched
        ]

        if invalid_keys:
            raise KeyError(
                f"The following free texts were not found among the unmatched strings: {invalid_keys}."
            )

        for free_text, match in matchings.items():
            self.match(free_text, match)

    # ---------------- OUTPUTTING RESULTS ----------------

    def output_results(self, output_dir: Path):
        results_dir: Path = output_dir / f"deft_matcher_{self.uuid}"
        results_dir.mkdir(parents=True, exist_ok=False)

        self.logger.info(f"Outputting DEFTMatcher results to folder {results_dir}.")

        results_df: DataFrame = self.create_results_df()
        metadata: MetaData = self.create_metadata(self.uuid)

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
                }
                for free_text, data in self.matchings.items()
            ]
        )
        return df

    def create_metadata(self, matching_uuid: str) -> MetaData:
        matchers_applied: list[Matcher] = self.matchers[0 : self.next_index]

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
            unique_free_texts_matched_by_matcher=self.get_unique_free_texts_by_matcher(),
        )

        metadata = MetaData(
            data_name=self.data_name,
            time_started=self.time_started,
            time_created=datetime.now().strftime("%d-%m-%Y_%H-%M-%S"),
            matchers=[matcher.name for matcher in matchers_applied],
            matching_uuid=matching_uuid,
            statistics=statistics,
            unique_unmatched_free_texts=list(self.unmatched),
        )

        return metadata

    def get_unique_free_texts_by_matcher(self) -> dict[str, int]:
        count_dict: dict[str, int] = {}

        for match_data in self.matchings.values():
            matcher_name = match_data.matcher_name
            count_dict[matcher_name] = count_dict.get(matcher_name, 0) + 1

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
        header_str = (
            f"Applying the DEFTMatcher pipeline to {self.data_name} with matchers:\n"
        )
        matcher_str = "\n".join(f"  - {matcher.name}" for matcher in self.matchers)
        return header_str + matcher_str

    @staticmethod
    def startup_from_file_log_str(
        matching_file_path: str, metadata_file_path: str
    ) -> str:
        return f"DeftMatcher object loaded from {matching_file_path} and {metadata_file_path}"

    def log_new_matcher(self, matcher_name: str):
        self.logger.info(
            f"Applying matcher {matcher_name} to {len(self.unmatched)} unmatched strings."
        )

    def log_match_info(self, matcher_name: str, solved: list[str]):
        """Logs our progress after applying a matcher."""

        log_parts = [
            self.header_log_str(matcher_name),
            self.solved_log_str(solved, 3),
            self.unsolved_log_str(3),
            self.footer_log_str(),
        ]

        self.logger.info("\n".join(log_parts))

    @staticmethod
    def header_log_str(matcher_name: str) -> str:
        return f"Matcher {matcher_name} was successfully applied."

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
        if self.no_more_matchers():
            return self.no_more_matchers_str()
        else:
            return f"The next matcher is {self.next_matcher.name}."

    @staticmethod
    def example_match_str(text: str, text_match: str) -> str:
        return f"'{text}' → '{text_match}'"

    @staticmethod
    def no_more_matchers_str() -> str:
        return "There are no more matchers!"
