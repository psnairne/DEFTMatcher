from deft_matcher.matchers.human_matcher import HumanRetriever
from scripts.fixtures import hpo_candidate_retriever, hpo_console_interface


def main():
    human_matcher = HumanRetriever(hpo_console_interface(), hpo_candidate_retriever())

    human_matcher.get_matches("My leg hurts a lot")


if __name__ == "__main__":
    main()
