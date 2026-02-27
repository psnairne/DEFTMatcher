from pathlib import Path
import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import (
    hpo_exact_dm,
    hpo_syn_dm,
    fast_hpo_cr_dm,
    mondo_exact_dm,
    mondo_syn_dm,
    fast_mondo_cr_dm,
    hpo_vector_similarity_dm,
    null_dm,
    human_dm_hpo,
    human_dm_mondo,
    mondo_vector_similarity_dm,
)


def cods() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    cohort_df = dfs["Cohort"]
    cod_col = cohort_df["Cause of Death"]
    cod_col = cod_col.dropna()
    return list(cod_col)


def main():
    config = DeftMatcherConfig(
        decisive_matchers=[
            mondo_exact_dm(),
            mondo_syn_dm(),
            human_dm_mondo(),
            null_dm(),
        ]
    )

    data = DeftMatcherData(free_texts=cods(), data_name="IDATA_CODS")

    cods_normaliser = DeftMatcher(config=config, data=data)

    cods_normaliser.run()
    cods_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
