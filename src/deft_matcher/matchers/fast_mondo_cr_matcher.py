import os

import hpotk
from FastHPOCR.HPOAnnotator import HPOAnnotator
import pandas as pd
from FastHPOCR.IndexMONDO import IndexMONDO
from hpotk import Ontology, OntologyType
from pandas import DataFrame, Series

from deft_matcher.matcher import Matcher
from pathlib import Path

from deft_matcher.ontology_class import OntologyClass
from deft_matcher.utils import get_oc


class FastMONDOCRMatcher(Matcher):
    """
    Uses the FastHPOCR algorithm and library to match text to MONDO terms.
    See:
    - https://academic.oup.com/bioinformatics/article/40/7/btae406/7698025
    - https://github.com/tudorgroza/fast_hpo_cr

    NOTE: if you want to change the indexConfig in some way,
    then you must delete the existing mondo.index file in the data_output_dir.
    """

    mondo_obo_path: str
    data_output_dir: str
    _mondo_index_path: Path
    _annotations_out_path: Path
    _annotator: HPOAnnotator
    _mondo: Ontology
    _id_to_term: dict[str, OntologyClass]

    def __init__(self, mondo_obo_path: str, data_output_dir: str) -> None:
        self.mondo_obo_path = mondo_obo_path
        self.data_output_dir = data_output_dir
        self._mondo_index_path = Path(self.data_output_dir + "/mondo.index")
        self._annotations_out_path = Path(
            self.data_output_dir + "/mondo_annotations.tsv"
        )
        self._annotator = self._initialise_annotator()
        self._mondo = self._initialise_mondo()
        self._id_to_term = self._initialise_id_to_term()

    def _create_new_index_file(self):
        if not self._mondo_index_path.exists():
            index_mondo = IndexMONDO(
                self.mondo_obo_path, self.data_output_dir, indexConfig={}
            )
            # NOTE: TAKES A WHILE - CIRCA 20 MINS
            index_mondo.index()

    def _initialise_annotator(self):
        self._create_new_index_file()
        return HPOAnnotator(self._mondo_index_path)

    @staticmethod
    def _initialise_mondo():
        store = hpotk.configure_ontology_store()
        mondo = store.load_ontology(
            ontology_type=OntologyType.MONDO,
            release="v2025-12-02",
            prefixes_of_interest={"MONDO"},
        )
        return mondo

    def _initialise_id_to_term(self) -> dict[str, OntologyClass]:
        return {term.identifier.value: get_oc(term) for term in self._mondo.terms}

    @property
    def name(self) -> str:
        return "FastMONDOCRMatcher"

    def get_matches(self, free_text: str) -> list[OntologyClass]:
        annotations = self._annotator.annotate(free_text)
        self._annotator.serialize(annotations, self._annotations_out_path)
        if os.path.getsize(self._annotations_out_path) == 0:
            return []
        else:
            df: DataFrame = pd.read_csv(
                self._annotations_out_path, sep="\t", header=None
            )
            mondo_id_col: Series = df[1]
            mondo_ids: list[str] = list(mondo_id_col)
            mondo_terms: list[OntologyClass] = [
                self._id_to_term[mondo_id] for mondo_id in mondo_ids
            ]
            return mondo_terms
