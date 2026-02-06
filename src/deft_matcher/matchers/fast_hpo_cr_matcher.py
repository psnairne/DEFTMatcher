import os

import hpotk
from FastHPOCR.HPOAnnotator import HPOAnnotator
from FastHPOCR.IndexHPO import IndexHPO
import pandas as pd
from hpotk import Ontology
from pandas import DataFrame, Series

from deft_matcher.matcher import Matcher
from pathlib import Path

from deft_matcher.ontology_class import OntologyClass


class FastHPOCRMatcher(Matcher):
    """
    Uses the FastHPOCR algorithm and library to match text to HPO terms.
    See:
    - https://academic.oup.com/bioinformatics/article/40/7/btae406/7698025
    - https://github.com/tudorgroza/fast_hpo_cr

    NOTE: if you want to change the indexConfig in some way,
    then you must delete the existing hp.index file in the data_output_dir.
    """

    hpo_obo_path: str
    data_output_dir: str
    _hpo_index_path: Path
    _annotations_out_path: Path
    _annotator: HPOAnnotator
    _hpo: Ontology
    _id_to_term: dict[str, OntologyClass]

    def __init__(self, hpo_obo_path: str, data_output_dir: str) -> None:
        self.hpo_obo_path = hpo_obo_path
        self.data_output_dir = data_output_dir
        self._hpo_index_path = Path(self.data_output_dir + "/hp.index")
        self._annotations_out_path = Path(self.data_output_dir + "/hpo_annotations.tsv")
        self._annotator = self._initialise_annotator()
        self._hpo = self._initialise_hpo()
        self._id_to_term = self._initialise_id_to_term()

    def _create_new_index_file(self):
        if not self._hpo_index_path.exists():
            index_config = {"rootConcepts": ["HP:0000118"]}
            index_hpo = IndexHPO(
                self.hpo_obo_path, self.data_output_dir, indexConfig=index_config
            )
            index_hpo.index()

    def _initialise_annotator(self):
        self._create_new_index_file()
        return HPOAnnotator(self._hpo_index_path)

    @staticmethod
    def _initialise_hpo() -> Ontology:
        store = hpotk.configure_ontology_store()
        return store.load_hpo(release="v2025-05-06")

    def _initialise_id_to_term(self) -> dict[str, OntologyClass]:
        return {
            term.identifier.value: OntologyClass.from_minimal_term(term)
            for term in self._hpo.terms
        }

    @property
    def name(self) -> str:
        return "FastHPOCRMatcher"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        annotations = self._annotator.annotate(free_text)
        self._annotator.serialize(annotations, self._annotations_out_path)
        if os.path.getsize(self._annotations_out_path) == 0:
            return []
        else:
            df: DataFrame = pd.read_csv(
                self._annotations_out_path, sep="\t", header=None
            )
            hpo_id_col: Series = df[1]
            hpo_ids: list[str] = list(hpo_id_col)
            hpo_terms: list[OntologyClass] = [
                self._id_to_term[hpo_id] for hpo_id in hpo_ids
            ]
            return hpo_terms
