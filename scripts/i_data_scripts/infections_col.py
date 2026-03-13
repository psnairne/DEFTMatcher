from pathlib import Path
import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import (
    mondo_exact_matcher,
    mondo_syn_matcher,
    fast_mondo_cr_matcher,
    hpo_exact_matcher,
    hpo_syn_matcher,
    fast_hpo_cr_matcher,
    hpo_vec_similarity_matcher,
)


def infections() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    infections_df = dfs["Infections"]
    infections_col = infections_df["Infection"]
    return list(infections_col)


def main():
    config = DeftMatcherConfig(
        matchers=[
            mondo_exact_matcher(),
            mondo_syn_matcher(),
            fast_mondo_cr_matcher(),
            hpo_exact_matcher(),
            hpo_syn_matcher(),
            fast_hpo_cr_matcher(),
            hpo_vec_similarity_matcher(similarity_threshold=0.7),
        ]
    )

    data = DeftMatcherData(free_texts=infections(), data_name="IDATA_INFECTIONS")

    infections_normaliser = DeftMatcher(config=config, data=data)

    infections_normaliser.run()
    infections_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
