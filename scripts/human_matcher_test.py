from deft_matcher.matchers.human_matcher import HumanMatcher
from deft_matcher.matchers.vector_similarity_matcher import HpoVectorSimilarityMatcher
from deft_matcher.matchers.human_matcher.user_interfaces import ConsoleInterface
from deft_matcher.matchers.human_matcher.user_interfaces import UserInterface


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

    blah = human_matcher.get_matches("My leg hurts a lot")

    print(f"SUCCESS: {blah}")


if __name__ == "__main__":
    main()
