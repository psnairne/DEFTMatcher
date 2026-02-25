from deft_matcher.matchers.fast_mondo_cr_matcher import FastMONDOCRMatcher
from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.human_matcher.user_interfaces.console_interface import (
    ConsoleInterface,
)
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)


def main():
    mondo_obo_path = "../tests/assets/ontology_obo_files/mondo_v2026-02-03.obo"
    ontology_prefix = "mondo"
    root_term = "MONDO:0000001"

    interface: UserInterface = ConsoleInterface(
        ontology_prefix=ontology_prefix,
        ontology_obo_path=mondo_obo_path,
        root_term=root_term,
    )

    candidate_retriever = FastMONDOCRMatcher(
        mondo_obo_path,
        root_term=root_term,
        data_output_dir="../tests/assets/fast_hpo_cr_data",
    )

    human_matcher = HumanMatcher(interface, candidate_retriever)

    human_matcher.get_matches("cystic fibrosis and also nutritional disorder")


if __name__ == "__main__":
    main()
