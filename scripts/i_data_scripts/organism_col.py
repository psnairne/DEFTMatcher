from pathlib import Path
import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from deft_matcher.matchers.null_matcher import NullMatcher
from scripts.fixtures import (
    ncit_exact_matcher,
    ncit_syn_matcher,
    ncit_vec_similarity_matcher,
    ncit_human_matcher,
    null_matcher,
)


def organisms() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    infections_df = dfs["Infections"]
    organisms_col = infections_df["Organism"]
    return list(organisms_col)


def main():
    # config = DeftMatcherConfig(
    #     matchers=[
    #         ncit_exact_matcher(),
    #         ncit_syn_matcher(),
    #         ncit_vec_similarity_matcher(similarity_threshold=0.85),
    #         ncit_human_matcher(5),
    #     ]
    # )
    #
    # data = DeftMatcherData(free_texts=organisms(), data_name="IDATA_ORGANISMS")
    #
    # organisms_normaliser = DeftMatcher(config=config, data=data)
    #
    # organisms_normaliser.run()
    # organisms_normaliser.output_results(
    #     Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    # )

    organisms_normaliser = DeftMatcher.load_state_from_files(
        matching_file_path="/Users/patrick/Downloads/I_DATA/alias_csv_files/deft_matcher_b4a23cd0-62b5-4958-9849-6afa47a235b1/matchings.csv",
        metadata_file_path="/Users/patrick/Downloads/I_DATA/alias_csv_files/deft_matcher_b4a23cd0-62b5-4958-9849-6afa47a235b1/metadata.json",
        matchers=[null_matcher()],
    )

    organisms_normaliser.run()
    organisms_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
