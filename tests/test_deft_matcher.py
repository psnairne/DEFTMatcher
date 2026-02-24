import tempfile
from pathlib import Path

import pytest
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_exact_dm, hpo_syn_dm


@pytest.fixture
def conditions() -> list[str]:
    return ["asthma", "osthma", "pneumonia", "osthma", "pneumonio"]


@pytest.fixture
def example_oc() -> OntologyClass:
    return OntologyClass("example_id", "example_label")


def test_deft_matcher(conditions):
    config = DeftMatcherConfig(decisive_matchers=[hpo_exact_dm()])

    data = DeftMatcherData(free_texts=conditions, data_name="example_data")

    deft_matcher = DeftMatcher(config=config, data=data)

    deft_matcher.run()

    assert len(deft_matcher.matchings) == 2
    assert len(deft_matcher.unmatched) == 1


def test_output_results(conditions):
    config = DeftMatcherConfig(decisive_matchers=[hpo_exact_dm()])

    data = DeftMatcherData(free_texts=conditions, data_name="example_data")

    deft_matcher = DeftMatcher(config=config, data=data)

    deft_matcher.run()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        deft_matcher.output_results(tmp_path)

        folder_name = f"deft_matcher_{deft_matcher.uuid}"

        matchings_file = tmp_path / folder_name / "matchings.csv"
        metadata_file = tmp_path / folder_name / "metadata.json"

        assert matchings_file.exists()
        assert metadata_file.exists()


def test_load_from_state():
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/metadata.json",
        decisive_matchers=[hpo_syn_dm()],
    )

    assert len(deft_matcher.matchings) == 2
    assert len(deft_matcher.unmatched) == 2
    assert len(deft_matcher.decisive_matchers) == 1


def test_rematch(example_oc):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/metadata.json",
        decisive_matchers=[hpo_syn_dm()],
    )

    deft_matcher.rematch("asthma", example_oc)

    assert deft_matcher.matchings["asthma"].match == example_oc


def test_rematch_fail(example_oc):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/metadata.json",
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.rematch("osthma", example_oc)


def test_bulk_rematch(example_oc):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/metadata.json",
        decisive_matchers=[hpo_syn_dm()],
    )

    deft_matcher.bulk_rematch({"asthma": example_oc, "pneumonia": example_oc})

    assert deft_matcher.matchings["asthma"].match == example_oc
    assert deft_matcher.matchings["pneumonia"].match == example_oc


def test_bulk_rematch_fail(example_oc):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/metadata.json",
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.bulk_rematch({"osthma": example_oc, "pneumonio": example_oc})


def test_match(example_oc):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/metadata.json",
        decisive_matchers=[hpo_syn_dm()],
    )

    deft_matcher.match("osthma", example_oc)

    assert len(deft_matcher.matchings) == 3
    assert len(deft_matcher.unmatched) == 1
    assert "osthma" in deft_matcher.matchings
    assert "osthma" not in deft_matcher.unmatched


def test_match_fail(example_oc):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/metadata.json",
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.match("asthma", example_oc)


def test_bulk_match(example_oc):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/metadata.json",
        decisive_matchers=[hpo_syn_dm()],
    )

    deft_matcher.bulk_match({"osthma": example_oc, "pneumonio": example_oc})

    assert len(deft_matcher.matchings) == 4
    assert len(deft_matcher.unmatched) == 0
    assert "osthma" in deft_matcher.matchings
    assert "pneumonio" in deft_matcher.matchings


def test_bulk_match_fail(example_oc):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/matchings.csv",
        metadata_file_path="/Users/patrick/DEFTMatcher/tests/assets/test_deft_matcher_output/metadata.json",
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.bulk_match({"asthma": example_oc, "pneumonia": example_oc})
