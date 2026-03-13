from deft_matcher.matcher import Matcher
from deft_matcher.ontology_class import OntologyClass


class FromCsvMatcher(Matcher):
    """
    Uses a previously created matchings.csv file to match the free text to the OntologyClass.
    """

    null_ontology_class: OntologyClass

    def __init__(
        self,
        csv_file_path: str,
        free_text_col_name: str,
        ontology_class_id_col_name: str,
        ontology_class_label_col_name: str,
        matcher_col_name: str,
    ) -> None:
        self.csv_file_path = csv_file_path
        self.free_text_col_name = free_text_col_name
        self.ontology_class_id_col_name = ontology_class_id_col_name
        self.ontology_class_label_col_name = ontology_class_label_col_name
        self.matcher_col_name = matcher_col_name

    @property
    def name(self) -> str:
        return "FromCsvMatcher"

    def match(self, free_text: str) -> OntologyClass | None:
        return self.null_ontology_class
