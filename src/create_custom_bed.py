#!/usr/bin/env python3

import polars as pl

LOCI_BUFFER_SIZE = 5000

mitocarta = (pl
    .read_csv(source="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/human_gene_id_from_mito_carta3.0_ensembl_mapping.txt",
        has_header=True,
        separator="\t"
    )
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
)

# Replace MT with chrM
fosiwiki = (pl
            .read_csv(source="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/GenomeLoci_MITOMAP_Foswiki_ensembl_mapping.txt",
                       has_header=True,
                       separator="\t"
            )
            .with_columns(pl.lit("chrM").alias("chromosome_or_scaffold_name"))
)

bed = (mitocarta 
    .vstack(fosiwiki)
    .select(["chromosome_or_scaffold_name", "gene_start", "gene_end"])
    .sort(by=["chromosome_or_scaffold_name", "gene_start", "gene_end"])
)

bed.write_csv(file="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/custom.bed",
              separator="\t",
              has_header=False)

