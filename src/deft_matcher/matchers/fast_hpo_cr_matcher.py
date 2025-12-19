import os

from FastHPOCR.HPOAnnotator import HPOAnnotator
from FastHPOCR.IndexHPO import IndexHPO
import pandas as pd

from deft_matcher.matcher import Matcher
from pathlib import Path


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

    def __init__(self, hpo_obo_path: str, data_output_dir: str) -> None:
        self.hpo_obo_path = hpo_obo_path
        self.data_output_dir = data_output_dir
        self._hpo_index_path = Path(self.data_output_dir + "/hp.index")
        self._annotations_out_path = Path(self.data_output_dir + "/hpo_annotations.tsv")
        self._annotator = self._initialise_annotator()

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

    @property
    def name(self) -> str:
        return "FastHPOCRMatcher"

    def get_matches(self, free_text: str) -> list[str]:
        annotations = self._annotator.annotate(free_text)
        self._annotator.serialize(annotations, self._annotations_out_path)
        if os.path.getsize(self._annotations_out_path) == 0:
            return []
        else:
            df = pd.read_csv(self._annotations_out_path, sep="\t", header=None)
            hpo_id_col = df[1]
            return list(hpo_id_col)
