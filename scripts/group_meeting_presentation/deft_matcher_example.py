from pathlib import Path

import pandas as pd

from deft_matcher.deft_matcher import DeftMatcherConfig, DeftMatcherData, DeftMatcher
from scripts.fixtures import (
    hpo_exact_matcher,
    hpo_syn_matcher,
    hpo_vec_similarity_matcher,
    hpo_human_matcher,
)


def main():
    data = DeftMatcherData(
        free_texts=pd.read_csv("messy_data.csv")["PHENOTYPES"].tolist(),
        data_name="messy_immune_disease_data",
    )
    config = DeftMatcherConfig(
        matchers=[
            hpo_exact_matcher(),
            hpo_syn_matcher(),
            hpo_vec_similarity_matcher(similarity_threshold=0.7),
            hpo_human_matcher(number_of_candidates=5),
        ]
    )

    deft_matcher = DeftMatcher(data=data, config=config)

    deft_matcher.run()

    deft_matcher.output_results(Path("output_dir"))


if __name__ == "__main__":
    main()
