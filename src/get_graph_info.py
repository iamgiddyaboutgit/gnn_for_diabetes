#!/usr/bin/env python3

import polars as pl

LOCI_BUFFER_SIZE = 5000

string_mapping = (pl
    .read_csv(source="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/string_mapping.tsv",
            has_header=True,
            separator="\t")
    .rename({"queryItem": "gene_name"})
)

string_interactions = (pl
    .read_csv(source="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/string_interactions_50_2nd_shell.tsv",
            has_header=True,
            separator="\t",
            infer_schema_length=100000)
    .select(["#node1", "node2", "combined_score"])
)

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

gene_and_node = (mitocarta 
    .vstack(fosiwiki)
    .sort(by=["chromosome_or_scaffold_name", "gene_start", "gene_end"])
    .with_row_count(offset=0)
    .with_columns([
        pl.col("row_nr").alias("node_num")
    ])
    .select(["gene_name", "node_num"])
    .unique()
)

# There are some isolated nodes.
# print(gene_and_node.filter(pl.col("gene_name").is_null()))

graph_rep = (gene_and_node
    .join(other=string_interactions,
          left_on="gene_name",
          right_on="#node1",
          how="left"
    )
    .with_columns([
        pl.col("node_num").alias("node_A_num")
    ])
    .select(["node_A_num", "node2", "combined_score"])
    .unique(["node_A_num", "node2"])
    .join(other=gene_and_node,
        left_on="node2",
        right_on="gene_name",
        how="left")
    .with_columns([
        pl.col("node_num").alias("node_B_num")
    ])
    .select(["node_A_num", "node_B_num", "combined_score"])
    .unique(subset=["node_A_num", "node_B_num"])
)

graph_rep.write_csv(file="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/node_data_for_bed.txt",
                    has_header=True,
                    separator="\t")

