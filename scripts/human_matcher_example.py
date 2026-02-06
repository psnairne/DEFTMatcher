from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from deft_matcher.matchers.human_matcher.user_interfaces.console_interface_hpo import (
    ConsoleInterfaceHpo,
)
from deft_matcher.matchers.human_matcher.user_interfaces.user_interface import (
    UserInterface,
)
from deft_matcher.matchers.vector_similarity_matcher import HpoVectorSimilarityMatcher


def main():
    interface: UserInterface = ConsoleInterfaceHpo("v2025-11-24")

    embedded_hpo_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_embedded.npz"
    embedding_metadata_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/data/hpo_meta.json"
    embedding_model_path = "/Users/patrick/DEFTMatcher/src/deft_matcher/matchers/rag_hpo_matcher/sbert_model"

    candidate_retriever = HpoVectorSimilarityMatcher(
        embedded_hpo_path=embedded_hpo_path,
        embedding_metadata_path=embedding_metadata_path,
        embedding_model_path=embedding_model_path,
        similarity_threshold=0,
        max_candidates=3,
    )

    human_matcher = HumanMatcher(interface, candidate_retriever)

    human_matcher.get_matches("My leg hurts a lot")


if __name__ == "__main__":
    main()
