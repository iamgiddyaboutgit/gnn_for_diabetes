#!/usr/bin/env python3

import polars as pl

LOCI_BUFFER_SIZE = 5000

mitocarta = pl.read_csv(source="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/human_gene_id_from_mito_carta3.0_ensembl_mapping.txt",
            has_header=True,
            separator="\t"
)

# Replace MT with M
fosiwiki = (pl
            .read_csv(source="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/GenomeLoci_MITOMAP_Foswiki_ensembl_mapping.txt",
                       has_header=True,
                       separator="\t"
            )
            .with_columns(pl.lit("M").alias("chromosome_or_scaffold_name"))
)

mitocarta_and_fosiwiki = (mitocarta 
    .vstack(fosiwiki)
)

# mitocarta_and_fosiwiki_gene_stable_ids = (mitocarta 
#     .vstack(fosiwiki)
#     .select("gene_stable_id")
# )

# (mitocarta_and_fosiwiki_gene_stable_ids
#     .write_csv(file="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/mitocarta_and_fosiwiki_gene_stable_ids.txt",
#                has_header=False,
#                separator="\n")
# )


bed = (mitocarta 
    .vstack(fosiwiki)
    .filter(
        pl.col("chromosome_or_scaffold_name")
            .str.starts_with("C")
            .is_not()
    )
    .filter(
        pl.col("chromosome_or_scaffold_name")
            .str.starts_with("K")
            .is_not()
    )
    .with_columns([
        (pl.col("gene_start") - LOCI_BUFFER_SIZE).alias("gene_start"),

        (pl.col("gene_end") + LOCI_BUFFER_SIZE).alias("gene_end"),

        pl.col("chromosome_or_scaffold_name").str.replace("^", "chr").alias("chromosome_or_scaffold_name")
    ])
    .select(["chromosome_or_scaffold_name", "gene_start", "gene_end"])
    .vstack(mt_stuff)
)

bed.write_csv(file="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/custom.bed",
              separator="\t",
              has_header=False)

