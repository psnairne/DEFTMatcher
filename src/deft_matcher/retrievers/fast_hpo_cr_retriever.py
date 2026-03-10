import os
from typing import Iterable

from FastHPOCR.HPOAnnotator import HPOAnnotator
from FastHPOCR.IndexHPO import IndexHPO
import pandas as pd
from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface
from pandas import DataFrame, Series

from deft_matcher.retriever import Retriever
from pathlib import Path

from deft_matcher.utils import validate_file_path_has_version_and_return
from deft_matcher.ontology_class import OntologyClass


class FastHPOCRRetriever(Retriever):
    """
    Uses the FastHPOCR algorithm and library to match text to HPO terms.
    See:
    - https://academic.oup.com/bioinformatics/article/40/7/btae406/7698025
    - https://github.com/tudorgroza/fast_hpo_cr

    NOTE: if you want to change the indexConfig in some way,
    then you must delete the existing hp.index file in the data_output_dir.
    """

    hpo_obo_path: str
    root_term: str
    hpo_version: str
    data_output_dir: str
    _oak_ontology_str: str
    _hpo: OboGraphInterface
    _hpo_index_path: Path
    _annotations_out_path: Path
    _annotator: HPOAnnotator
    _id_to_term: dict[str, OntologyClass]

    def __init__(self, hpo_obo_path: str, root_term: str, data_output_dir: str) -> None:
        self.hpo_obo_path = hpo_obo_path
        self.root_term = root_term
        self.data_output_dir = data_output_dir
        self.hpo_version = validate_file_path_has_version_and_return(self.hpo_obo_path)
        self._oak_ontology_str = self._initialise_oak_ontology_str()
        self._hpo = self._initialise_hpo()
        self._hpo_index_path = Path(
            self.data_output_dir + "/hp_" + self.hpo_version + ".index"
        )
        self._annotations_out_path = Path(
            self.data_output_dir + "/hp_annotations_" + self.hpo_version + ".tsv"
        )
        self._annotator = self._initialise_annotator()
        self._id_to_term = self._initialise_id_to_term()

    def _initialise_oak_ontology_str(self) -> str:
        return "simpleobo:" + self.hpo_obo_path

    def _initialise_hpo(self) -> OboGraphInterface:
        return get_adapter(self._oak_ontology_str)

    def _create_new_index_file(self):
        if not self._hpo_index_path.exists():
            index_config = {"rootConcepts": [self.root_term]}
            index_hpo = IndexHPO(
                self.hpo_obo_path, self.data_output_dir, indexConfig=index_config
            )
            index_hpo.index()

            old_path = os.path.join(self.data_output_dir, "hp.index")
            new_file_name = f"hp_{self.hpo_version}.index"
            new_path = os.path.join(self.data_output_dir, new_file_name)

            if os.path.exists(old_path):
                os.rename(old_path, new_path)
            else:
                raise FileNotFoundError(f"File not found: {old_path}")

    def _initialise_annotator(self):
        self._create_new_index_file()
        return HPOAnnotator(self._hpo_index_path)

    def _initialise_id_to_term(self) -> dict[str, OntologyClass]:
        all_term_ids: Iterable[str] = self._hpo.descendants(
            self.root_term, predicates=[IS_A]
        )
        id_to_term: dict[str, OntologyClass] = dict()
        for term_id in all_term_ids:
            id_to_term[term_id] = OntologyClass.from_term_id(term_id, self._hpo)
        return id_to_term

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
