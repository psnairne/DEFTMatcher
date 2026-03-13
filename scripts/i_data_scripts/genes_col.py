from pathlib import Path

import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import (
    null_matcher,
    hgnc_exact_matcher,
    hgnc_syn_matcher,
    hgnc_human_matcher,
)


def genes() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    cohort_df = dfs["Cohort"]
    cohort_gene_col_1 = cohort_df["Gene Mutation"]
    cohort_gene_col_2 = cohort_df["Other Mutation"]
    molecular_info_df = dfs["Molecular Info"]
    molecular_info_gene_col = molecular_info_df["Gene Mutation"]
    all_genes = list(
        set().union(cohort_gene_col_1, cohort_gene_col_2, molecular_info_gene_col)
    )
    return all_genes


def main():
    config = DeftMatcherConfig(
        matchers=[
            hgnc_exact_matcher(),
            hgnc_syn_matcher(),
            hgnc_human_matcher(number_of_candidates=5),
            null_matcher(),
        ]
    )

    data = DeftMatcherData(free_texts=genes(), data_name="IDATA_GENES")

    genes_normaliser = DeftMatcher(config=config, data=data)

    genes_normaliser.apply_matchings_in_csv(
        "/Users/patrick/Downloads/I_DATA/alias_csv_files/all_genes/matchings.csv"
    )

    genes_normaliser.run()

    genes_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
