#!/usr/bin/env python3

import polars as pl

genomic_loci_list_before_interactions_biomart_export = pl.read_csv(source="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/genomic_loci_list_before_interactions_biomart_export.txt",
            has_header=True,
            separator="\t"
)

