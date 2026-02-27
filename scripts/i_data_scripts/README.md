from scripts.fixtures import hpo_console_interface

# How to use DEFTMatcher

<!-- TOC -->
* [How to use DEFTMatcher](#how-to-use-deftmatcher)
  * [Example case](#example-case)
    * [Load the data](#load-the-data)
    * [Configure which decisive matchers you want to use](#configure-which-decisive-matchers-you-want-to-use)
    * [Configure the data](#configure-the-data)
    * [Run the pipeline and output the results.](#run-the-pipeline-and-output-the-results)
  * [Loading and editing a previous pipeline](#loading-and-editing-a-previous-pipeline)
  * [Matchers, Resolvers and DecisiveMatchers](#matchers-resolvers-and-decisivematchers)
    * [ExactMatcher](#exactmatcher)
    * [SynonymMatcher](#synonymmatcher)
    * [FastHPOCRMatcher](#fasthpocrmatcher)
    * [FastMONDOCRMatcher](#fastmondocrmatcher)
    * [VectorSimilarityMatcher](#vectorsimilaritymatcher)
    * [HumanMatcher](#humanmatcher)
    * [NullMatcher](#nullmatcher)
<!-- TOC -->

## Example case

Here is how the pipeline is used in practice:

```python

from pathlib import Path

import pandas as pd
from deft_matcher.deft_matcher import DeftMatcher, DeftMatcherConfig, DeftMatcherData
from scripts.fixtures import (
    hpo_exact_dm,
    hpo_syn_dm,
    null_dm,
    human_dm_hpo,
)


def conditions() -> list[str]:
    dfs = pd.read_excel("I_DATA/i_data.xlsx", sheet_name=None)
    conditions_df = dfs["Conditions"]
    conditions_col = conditions_df["Condition"]
    return list(conditions_col)


def main():
    config = DeftMatcherConfig(
        decisive_matchers=[
            hpo_exact_dm(),
            hpo_syn_dm(),
            human_dm_hpo(),
            null_dm(),
        ]
    )

    data = DeftMatcherData(free_texts=conditions(), data_name="IDATA_CONDITIONS")

    conditions_normaliser = DeftMatcher(config=config, data=data)

    conditions_normaliser.run()
    conditions_normaliser.output_results(
        Path("output/dir")
    )


if __name__ == "__main__":
    main()
```

I will go through these parts one by one.

### Load the data

We need a list of strings. Maybe you need to do `.dropna()` so that we don't get that nan error. Or feel free to edit
the
DEFTMatcher code so that there is a check in the DEFTMatcher object that the input is actually strings (so that it
throws an error immediately and doesn't waste time).

```python
def conditions() -> list[str]:
    dfs = pd.read_excel("I_DATA/i_data.xlsx", sheet_name=None)
    conditions_df = dfs["Conditions"]
    conditions_col = conditions_df["Condition"]
    return list(conditions_col)
```

### Configure which decisive matchers you want to use

```python
config = DeftMatcherConfig(
    decisive_matchers=[
        hpo_exact_dm(),
        hpo_syn_dm(),
        human_dm_hpo(),
        null_dm(),
    ]
)
```

A decisive matcher is something which matches a free text to an `OntologyClass`. An `OntologyClass` is a class in this
project which simply consists of two attributes: a CURIE_ID and a label.

Look in the `scripts/fixtures.py` file for the decisive matchers that I have already written.

The order of the list above will determine the order in which the matchers are applied to the input texts.

### Configure the data

```python
data = DeftMatcherData(free_texts=conditions(), data_name="IDATA_CONDITIONS")
```

This is just a wrapper around the free_texts. It's given a `data_name` just to make the logging prettier.

### Run the pipeline and output the results.

```python
conditions_normaliser = DeftMatcher(config=config, data=data)

conditions_normaliser.run()
conditions_normaliser.output_results(
    Path("output/dir")
)
```

Here we create the object, run the pipeline and output the results. Into the folder `output/dir` you will find a new
folder called `deft_matcher_uuid`. Inside that will be two files: `matchings.csv` and `metadata.json`.

Inside `matchings.csv` you will find all the matchings. This can be linked up directly to the PhenoXtract pipeline.
Inside `metadata.json` you will find other statistics and info. In particular, you will also find the strings you did
not match.

## Loading and editing a previous pipeline

If you notice an error in `matchings.csv`, or `metadata.json`, for example an unmatched string that should have a match,
or a match that is clearly false, you can load up a DEFTMatcher pipeline from that state, and then either apply a new
list of decisive matchers, or directly edit the internal state of the pipeline. Here is how you do that:

```python
old_state = DeftMatcher.load_state_from_files(
    ".../I_DATA/alias_csv_files/infections/matchings.csv",
    ".../I_DATA/alias_csv_files/infections/metadata.json",
    [mondo_vector_similarity_dm(), human_dm_mondo()],
)

# you can unmatch individual strings
old_state.unmatch("NA")
old_state.unmatch("Bad Data")
# you can do this in bulk as well
old_state.bulk_unmatch(["blah", "blahblah"])

# you can make new matches
old_state.match("morfan syndr", OntologyClass("MONDO:0007947", "Marfan syndrome"))
# and you can do this in bulk
old_state.bulk_match({"maefan syndrom": OntologyClass("MONDO:0007947", "Marfan syndrome"),
                      "disase": OntologyClass("MONDO:0000001", "disease")})

# .rematch() and .bulk_rematch() work in exactly the same way, 
# except they will make changes to existing matches.

# This will run the decisive matchers you loaded up the state with. 
# In this case it will run mondo_vector_similarity_dm() followed by human_dm_mondo()
old_state.run()

# and you can output the results again. The UUID will be different therefore you will get new files. 
old_state.output_results(Path("/Users/patrick/Downloads/I_DATA/alias_csv_files"))
```

## Matchers, Resolvers and DecisiveMatchers

A Matcher takes a free text and returns a `list[OntologyClass]`. A resolver takes a `list[OntologyClass]` and returns an
`OntologyClass`. A DecisiveMatcher is just a Matcher together with a Resolver. I have preconfigured various of these in
the `scripts/fixtures.py` file.

### ExactMatcher

You can input whatever ontology you like, but you need the OBO file. Does matches based on mapping Ontology class names
to their IDs.

### SynonymMatcher

The same as above but allows synonyms. Filtering of synonym types is currently not implemented.

### FastHPOCRMatcher

A matching algorithm which heavily relies on token overlap and similar ideas. Have a look at the FastHPOCR paper for
more information. A preconfigured dictionary/index is required. This is what the hp_annotations_vYYYY-MM-DD.index file
is for. If you do not provide this, it will be created fresh, which will take a while.

It is, as the name says, very quick.

### FastMONDOCRMatcher

The same as above. It will take a while to create the index file.

### VectorSimilarityMatcher

Makes matches based on vector similarity. The example I have been using is this: it can map "my leg hurts" to "Lower
Limb Pain" in the HPO.

You can apply this for any ontology you like, but you need:

1. The Ontology .OBO file.
2. An embeddings.npz file
3. An embeddings_metadata.json file. This is needed so we can figure out what ontology classes the vectors correspond
   to. Speak to Peter H if you want more details on how to make these embeddings files, we were collaborating on that.
4. An embedding model. This needs to be the same as the embedding model used to create the embeddings.npz file and
   metadata.json files.

The `root_term` field is useful if you want to ignore parts of the ontology. For example, for HPO you probably only want
descendants of Phenotypic Abnormality.

Experiment with the `similarity_threshold`. The higher is better, but good matches are also made with a threshold of 0.6
I have seen.

### HumanMatcher

This is set-up as follows

```python
hpo_console_interface = ConsoleInterface(
    ontology_prefix="hp",
    ontology_obo_path=hpo_obo_path(),
    # phenotypic abnormality
    root_term="HP:0000118",
)

hpo_candidate_retriever = VectorSimilarityMatcher(
    embedding_path=embedded_hpo_path(),
    embedding_metadata_path=hpo_embedding_metadata_path(),
    embedding_model_path=embedding_model_path(),
    similarity_threshold=0,
    max_candidates=5,
    ontology_obo_path=hpo_obo_path(),
    ontology_prefix="hp",
    # phenotypic abnormality
    root_term="HP:0000118",
)

human_matcher = HumanMatcher(
    interface=hpo_console_interface(), candidate_retriever=hpo_candidate_retriever()
)
```

The `console_interface` governs what the user actually sees. Keeping this modular allowed me to mock it for tests.

The `candidate_retriever` can be any matcher, since all a Matcher does is return a list of strings. But a sensible
choice is the one I have given above.

### NullMatcher

For PhenoXtract, it can be convenient to map free texts to completely empty ontology classes. In the CSV this will just
be empty strings. The NullMatcher simply matches every remaining text to the empty ontology class OntologyClass(,).
There's also a ConstantMatcher, which works in the obvious way, if you want to map free_texts to a specific
OntologyClass of your choosing.