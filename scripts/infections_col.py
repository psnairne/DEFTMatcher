from pathlib import Path
import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import mondo_exact_dm, mondo_syn_dm, fast_mondo_cr_dm, null_dm


def infections() -> list[str]:
    dfs = pd.read_excel("/Users/patrick/Downloads/I_DATA/i_data.xlsx", sheet_name=None)
    infections_df = dfs["Infections"]
    infections_col = infections_df["Infection"]
    return list(infections_col)


def main():
    config = DeftMatcherConfig(
        decisive_matchers=[
            mondo_exact_dm(),
            mondo_syn_dm(),
            fast_mondo_cr_dm(),
            null_dm(),
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
