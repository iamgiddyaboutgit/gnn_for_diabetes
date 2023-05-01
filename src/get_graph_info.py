#!/usr/bin/env python3

import polars as pl

mcem = (pl
    .read_csv(source="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/human_gene_id_from_mito_carta3.0_ensembl_mapping.txt",
            has_header=True,
            separator="\t")
)

string_mapping = (pl
    .read_csv(source="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/string_mapping.tsv",
            has_header=True,
            separator="\t")
)

(mcem
    .join(other=string_mapping,
          on=["gene_name", "#queryIndex"],
          how="left")
    .head()
 )

