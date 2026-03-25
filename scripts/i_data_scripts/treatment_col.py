from pathlib import Path
import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import (
    maxo_exact_matcher,
    maxo_vec_similarity_matcher,
    maxo_syn_matcher,
    maxo_human_matcher,
    null_matcher,
)


def treatments() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    non_surg_procedures_df = dfs["Nonsurg Procedure"]
    treatment_col = non_surg_procedures_df["Treatment Name"]
    return list(treatment_col)


def main():
    config = DeftMatcherConfig(
        matchers=[
            maxo_exact_matcher(),
            maxo_syn_matcher(),
            maxo_vec_similarity_matcher(similarity_threshold=0.7),
            maxo_human_matcher(number_of_candidates=5),
            null_matcher(),
        ]
    )

    data = DeftMatcherData(free_texts=treatments(), data_name="IDATA_TREATMENTS")

    treatments_normaliser = DeftMatcher(config=config, data=data)

    treatments_normaliser.run()
    treatments_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
