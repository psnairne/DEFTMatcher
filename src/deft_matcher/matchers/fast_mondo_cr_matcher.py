import os

from FastHPOCR.HPOAnnotator import HPOAnnotator
import pandas as pd
from FastHPOCR.IndexMONDO import IndexMONDO

from deft_matcher.matcher import Matcher
from pathlib import Path


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

    def __init__(self, mondo_obo_path: str, data_output_dir: str) -> None:
        self.mondo_obo_path = mondo_obo_path
        self.data_output_dir = data_output_dir
        self._mondo_index_path = Path(self.data_output_dir + "/mondo.index")
        self._annotations_out_path = Path(
            self.data_output_dir + "/mondo_annotations.tsv"
        )
        self._annotator = self._initialise_annotator()

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

    @property
    def name(self) -> str:
        return "FastMONDOCRMatcher"

    def get_matches(self, free_text: str) -> list[str]:
        annotations = self._annotator.annotate(free_text)
        self._annotator.serialize(annotations, self._annotations_out_path)
        if os.path.getsize(self._annotations_out_path) == 0:
            return []
        else:
            df = pd.read_csv(self._annotations_out_path, sep="\t", header=None)
            hpo_id_col = df[1]
            return list(hpo_id_col)
