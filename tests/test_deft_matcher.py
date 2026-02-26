import tempfile
from pathlib import Path

import pytest
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from deft_matcher.matchers.exact_matcher import ExactMatcher
from deft_matcher.matchers.fast_hpo_cr_matcher import FastHPOCRMatcher
from deft_matcher.matchers.fast_mondo_cr_matcher import FastMONDOCRMatcher
from deft_matcher.matchers.null_matcher import NullMatcher
from deft_matcher.matchers.synonym_matcher import SynonymMatcher
from deft_matcher.matchers.vector_similarity_matcher.vector_similarity_matcher import (
    VectorSimilarityMatcher,
)


@pytest.fixture
def hpo_obo_path() -> str:
    return (
        "/Users/patrick/DEFTMatcher/tests/assets/ontology_obo_files/hp_v2026-02-16.obo"
    )


@pytest.fixture
def mondo_obo_path() -> str:
    return "/Users/patrick/DEFTMatcher/tests/assets/ontology_obo_files/mondo_v2026-02-03.obo"


@pytest.fixture
def data_output_dir() -> str:
    return "/Users/patrick/DEFTMatcher/tests/assets/fast_hpo_cr_data"


@pytest.fixture
def hpo_exact_matcher(hpo_obo_path):
    return ExactMatcher(
        "hp",
        hpo_obo_path,
        # phenotypic abnormality
        "HP:0000118",
    )


@pytest.fixture
def hpo_syn_matcher(hpo_obo_path):
    return SynonymMatcher(
        "hp",
        hpo_obo_path,
        # phenotypic abnormality
        "HP:0000118",
    )


@pytest.fixture
def mondo_exact_matcher(mondo_obo_path):
    return ExactMatcher(
        "mondo",
        mondo_obo_path,
        # disease
        "HP:0000001",
    )


@pytest.fixture
def mondo_syn_matcher(mondo_obo_path):
    return SynonymMatcher(
        "mondo",
        mondo_obo_path,
        # disease
        "MONDO:0000001",
    )
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_exact_dm, hpo_syn_dm


@pytest.fixture
def fast_hpo_cr_matcher(hpo_obo_path, data_output_dir) -> FastHPOCRMatcher:
    return FastHPOCRMatcher(
        hpo_obo_path=hpo_obo_path,
        data_output_dir=data_output_dir,
        root_term="HP:0000001",
    )
def conditions() -> list[str]:
    return ["asthma", "osthma", "pneumonia", "osthma", "pneumonio"]


@pytest.fixture
def fast_mondo_cr_matcher(mondo_obo_path, data_output_dir) -> FastMONDOCRMatcher:
    return FastMONDOCRMatcher(
        mondo_obo_path=mondo_obo_path,
        data_output_dir=data_output_dir,
        root_term="MONDO:0000001",
    )
def example_oc() -> OntologyClass:
    return OntologyClass("example_id", "example_label")


@pytest.fixture
def vector_similarity_matcher(hpo_obo_path) -> VectorSimilarityMatcher:
    embedded_hpo_path = "/Users/patrick/DEFTMatcher/tests/assets/vector_similarity_matcher_data/data/hpo_embedded.npz"
    embedding_metadata_path = "/Users/patrick/DEFTMatcher/tests/assets/vector_similarity_matcher_data/data/hpo_meta.json"
    embedding_model_path = "/Users/patrick/DEFTMatcher/tests/assets/vector_similarity_matcher_data/sbert_model"
    return VectorSimilarityMatcher(
        embedding_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
        similarity_threshold=0.75,
        ontology_obo_path=hpo_obo_path,
        ontology_prefix="hp",
        root_term="HP:0000001",
    )
def tests_dir() -> Path:
    return Path(__file__).parent


@pytest.fixture
def assets_dir(tests_dir) -> Path:
    return tests_dir / "assets"


@pytest.fixture
def test_deft_matcher_output_dir(assets_dir) -> Path:
    return assets_dir / "test_deft_matcher_output"


@pytest.fixture
def test_matchings_path(test_deft_matcher_output_dir) -> str:
    return str(test_deft_matcher_output_dir / "matchings.csv")


@pytest.fixture
def test_metadata_path(test_deft_matcher_output_dir) -> str:
    return str(test_deft_matcher_output_dir / "metadata.json")


def test_deft_matcher(conditions):
    config = DeftMatcherConfig(decisive_matchers=[hpo_exact_dm()])

    data = DeftMatcherData(free_texts=conditions, data_name="example_data")

    deft_matcher = DeftMatcher(config=config, data=data)

    deft_matcher.run()

    assert len(deft_matcher.matchings) == 2
    assert len(deft_matcher.unmatched) == 2


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


def test_load_from_state(test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    assert len(deft_matcher.matchings) == 2
    assert len(deft_matcher.unmatched) == 2
    assert len(deft_matcher.decisive_matchers) == 1


def test_rematch(example_oc, test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    deft_matcher.rematch("asthma", example_oc)

    assert deft_matcher.matchings["asthma"].match == example_oc


def test_rematch_fail(example_oc, test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.rematch("osthma", example_oc)


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipped in CI")
def test_deft_matcher_conditions_col(
    conditions,
    hpo_exact_matcher,
    hpo_syn_matcher,
    mondo_exact_matcher,
    mondo_syn_matcher,
    fast_hpo_cr_matcher,
    fast_mondo_cr_matcher,
    null_matcher,
    choose_first,
):
    hpo_exact_dm = DecisiveMatcher(
        matcher=hpo_exact_matcher, ambiguity_resolver=choose_first
def test_bulk_rematch(example_oc, test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    deft_matcher.bulk_rematch({"asthma": example_oc, "pneumonia": example_oc})

    assert deft_matcher.matchings["asthma"].match == example_oc
    assert deft_matcher.matchings["pneumonia"].match == example_oc


def test_bulk_rematch_fail(example_oc, test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.bulk_rematch({"osthma": example_oc, "pneumonia": example_oc})


def test_unmatch(test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    deft_matcher.unmatch("asthma")

    assert len(deft_matcher.matchings) == 1
    assert len(deft_matcher.unmatched) == 3
    assert "asthma" not in deft_matcher.matchings
    assert "asthma" in deft_matcher.unmatched


def test_unmatch_fail(test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.unmatch("osthma")


def test_bulk_unmatch(test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    deft_matcher.bulk_unmatch(["asthma", "pneumonia"])

    assert len(deft_matcher.matchings) == 0
    assert len(deft_matcher.unmatched) == 4


def test_bulk_unmatch_fail(test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.bulk_unmatch(["asthma", "pneumonio"])


def test_match(example_oc, test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    null_dm = DecisiveMatcher(matcher=null_matcher, ambiguity_resolver=choose_first)
    deft_matcher.match("osthma", example_oc)

    assert len(deft_matcher.matchings) == 3
    assert len(deft_matcher.unmatched) == 1
    assert "osthma" in deft_matcher.matchings
    assert "osthma" not in deft_matcher.unmatched


def test_match_fail(example_oc, test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.match("asthma", example_oc)

    config = DeftMatcherConfig(
        decisive_matchers=[
            hpo_exact_dm,
            hpo_syn_dm,
            fast_hpo_cr_dm,
            mondo_exact_dm,
            mondo_syn_dm,
            fast_mondo_cr_dm,
            null_dm,
        ]

def test_bulk_match(example_oc, test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )
    deft_matcher.bulk_match({"osthma": example_oc, "pneumonio": example_oc})

    assert len(deft_matcher.matchings) == 4
    assert len(deft_matcher.unmatched) == 0
    assert "osthma" in deft_matcher.matchings
    assert "pneumonio" in deft_matcher.matchings


def test_bulk_match_fail(example_oc, test_matchings_path, test_metadata_path):
    deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path=test_matchings_path,
        metadata_file_path=test_metadata_path,
        decisive_matchers=[hpo_syn_dm()],
    )

    with pytest.raises(KeyError):
        deft_matcher.bulk_match({"osthma": example_oc, "pneumonia": example_oc})
