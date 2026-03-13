from pathlib import Path
import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import mondo_exact_matcher, mondo_syn_matcher, null_matcher


def cods() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    cohort_df = dfs["Cohort"]
    cod_col = cohort_df["Cause of Death"]
    return list(cod_col)


def main():
    config = DeftMatcherConfig(
        matchers=[mondo_exact_matcher(), mondo_syn_matcher(), null_matcher()]
    )

    data = DeftMatcherData(free_texts=cods(), data_name="IDATA_CODS")

    cods_normaliser = DeftMatcher(config=config, data=data)

    cods_normaliser.run()
    cods_normaliser.output_results(
        Path("/Users/patrick/Downloads/I_DATA/alias_csv_files")
    )


if __name__ == "__main__":
    main()
