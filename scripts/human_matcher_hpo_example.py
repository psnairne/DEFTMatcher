from scripts.fixtures import hpo_human_matcher


def main():
    hpo_human_matcher(number_of_candidates=5).match("My leg hurts a lot")


if __name__ == "__main__":
    main()
