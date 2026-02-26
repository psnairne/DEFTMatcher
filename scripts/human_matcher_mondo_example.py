from deft_matcher.matchers.human_matcher.human_matcher import HumanMatcher
from scripts.fixtures import fast_mondo_cr_matcher, mondo_console_interface


def main():
    human_matcher = HumanMatcher(mondo_console_interface(), fast_mondo_cr_matcher())

    human_matcher.get_matches("cystic fibrosis and also nutritional disorder")


if __name__ == "__main__":
    main()
