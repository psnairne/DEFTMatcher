from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from scripts.fixtures import hpo_candidate_retriever, hpo_console_interface


def main():
    human_matcher = HumanMatcher(hpo_console_interface(), hpo_candidate_retriever())

    human_matcher.get_matches("My leg hurts a lot")


if __name__ == "__main__":
    main()
