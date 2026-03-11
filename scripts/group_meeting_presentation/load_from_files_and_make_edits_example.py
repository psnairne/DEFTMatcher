from pathlib import Path


from deft_matcher.deft_matcher import DeftMatcher
from deft_matcher.ontology_class import OntologyClass
from scripts.fixtures import hpo_exact_matcher


def main():
    new_deft_matcher = DeftMatcher.load_state_from_files(
        matching_file_path="output_dir/deft_matcher_be63077f-3b56-4ef0-817c-f597401d2249/matchings.csv",
        metadata_file_path="output_dir/deft_matcher_be63077f-3b56-4ef0-817c-f597401d2249/metadata.json",
        matchers=[hpo_exact_matcher()],
    )

    new_deft_matcher.rematch(
        free_text="pneumonia hx multiple",
        replacement_match=OntologyClass("HP:0006532", "Recurrent pneumonia"),
    )

    new_deft_matcher.unmatch("vaccinated against MMR")

    new_deft_matcher.run()

    new_deft_matcher.output_results(Path("output_dir"))


if __name__ == "__main__":
    main()
