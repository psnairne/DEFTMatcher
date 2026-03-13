from pathlib import Path
import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import hgnc_exact_matcher, hgnc_human_matcher, hgnc_syn_matcher


def genes() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    cohort_df = dfs["Cohort"]
    gene_col = cohort_df["Gene Mutation"]
    gene_col = gene_col.dropna()
    return list(gene_col)


def main():
    config = DeftMatcherConfig(
        matchers=[
            hgnc_exact_matcher(),
            hgnc_syn_matcher(),
            hgnc_human_matcher(number_of_candidates=5),
        ]
    )

    data = DeftMatcherData(free_texts=genes(), data_name="IDATA_GENES")

    genes_normaliser = DeftMatcher(config=config, data=data)

    genes_normaliser.run()
    genes_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
