from pathlib import Path
import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import mondo_exact_matcher, mondo_syn_matcher


def cancers() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    malignancies_df = dfs["Malignancies"]
    cancer_col = malignancies_df["cancer"]
    return list(cancer_col)


def main():
    config = DeftMatcherConfig(matchers=[mondo_exact_matcher(), mondo_syn_matcher()])

    data = DeftMatcherData(free_texts=cancers(), data_name="IDATA_CANCER")

    cancer_normaliser = DeftMatcher(config=config, data=data)

    cancer_normaliser.run()
    cancer_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
