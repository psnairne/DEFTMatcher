from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.human_matcher.user_interfaces.console_interface import (
    ConsoleInterface,
)
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)
from deft_matcher.matchers.vector_similarity_matcher.vector_similarity_matcher import (
    VectorSimilarityMatcher,
)


def main():
    hpo_obo_path = "../tests/assets/ontology_obo_files/hp_v2026-02-16.obo"
    embedded_hpo_path = (
        "../tests/assets/vector_similarity_matcher_data/data/hpo_embedded.npz"
    )
    embedding_metadata_path = (
        "../tests/assets/vector_similarity_matcher_data/data/hpo_meta.json"
    )
    embedding_model_path = "../tests/assets/vector_similarity_matcher_data/sbert_model"
    ontology_prefix = "hp"
    root_term = "HP:0000118"

    interface: UserInterface = ConsoleInterface(
        ontology_prefix=ontology_prefix,
        ontology_obo_path=hpo_obo_path,
        root_term=root_term,
    )

    candidate_retriever = VectorSimilarityMatcher(
        ontology_prefix=ontology_prefix,
        ontology_obo_path=hpo_obo_path,
        root_term=root_term,
        embedding_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
        similarity_threshold=0,
        max_candidates=4,
    )

    human_matcher = HumanMatcher(interface, candidate_retriever)

    human_matcher.get_matches("My leg hurts a lot")


if __name__ == "__main__":
    main()
