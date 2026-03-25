from pathlib import Path
import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import (
    null_matcher,
    maxo_exact_matcher,
    maxo_vec_similarity_matcher,
    maxo_syn_matcher,
)


def surgeries() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    surgeries_df = dfs["Surgeries"]
    surgery_col = surgeries_df["Surgery"]
    return list(surgery_col)


def main():
    config = DeftMatcherConfig(
        matchers=[
            maxo_exact_matcher(),
            maxo_syn_matcher(),
            maxo_vec_similarity_matcher(similarity_threshold=0.6),
            null_matcher(),
        ]
    )

    data = DeftMatcherData(free_texts=surgeries(), data_name="IDATA_SURGERIES")

    surgeries_normaliser = DeftMatcher(config=config, data=data)

    surgeries_normaliser.run()
    surgeries_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
