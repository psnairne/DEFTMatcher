from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from scripts.fixtures import fast_mondo_cr_retriever, mondo_console_interface


def main():
    human_matcher = HumanMatcher(mondo_console_interface(), fast_mondo_cr_retriever())

    human_matcher.match("cystic fibrosis and also nutritional disorder")


if __name__ == "__main__":
    main()
