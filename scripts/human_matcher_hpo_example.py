from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from scripts.fixtures import hpo_vec_similarity_retriever, hpo_console_interface


def main():
    human_matcher = HumanMatcher(
        hpo_console_interface(), hpo_vec_similarity_retriever()
    )

    human_matcher.match("My leg hurts a lot")


if __name__ == "__main__":
    main()
