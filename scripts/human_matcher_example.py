from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.human_matcher.user_interfaces.console_interface import (
    ConsoleInterface,
)
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)
from deft_matcher.matchers.vector_similarity_matcher import HpoVectorSimilarityMatcher


def main():
    interface: UserInterface = ConsoleInterface()

    embedded_hpo_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_embedded.npz"
    embedding_metadata_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_meta.json"
    embedding_model_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/sbert_model"

    candidate_retriever = HpoVectorSimilarityMatcher(
        embedded_hpo_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
        similarity_threshold=0,
        max_candidates=10,
    )

    human_matcher = HumanMatcher(interface, candidate_retriever)

    chosen_match = human_matcher.get_matches("My leg hurts a lot")[0]

    print("SUCCESS")
    print(f"YOU CHOSE: {chosen_match}")


if __name__ == "__main__":
    main()
