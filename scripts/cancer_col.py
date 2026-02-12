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
    vector_similarity_dm,
    null_dm,
)


def cancers() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    malignancies_df = dfs["Malignancies"]
    cancer_col = malignancies_df["cancer"]
    return list(cancer_col)


def main():
    config = DeftMatcherConfig(
        decisive_matchers=[
            hpo_exact_dm(),
            hpo_syn_dm(),
            fast_hpo_cr_dm(),
            mondo_exact_dm(),
            mondo_syn_dm(),
            fast_mondo_cr_dm(),
            vector_similarity_dm(),
            null_dm(),
        ]
    )

    data = DeftMatcherData(free_texts=cancers(), data_name="IDATA_CANCER")

    cancer_normaliser = DeftMatcher(config=config, data=data)

    cancer_normaliser.run()
    cancer_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
