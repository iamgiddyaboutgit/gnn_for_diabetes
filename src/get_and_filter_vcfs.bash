#!/usr/bin/env bash

aws s3 sync \
    --no-sign-request \
    --exclude="*" \
    --include="*.hard-filtered.vcf.gz*" \
    s3://1000genomes-dragen/data/dragen-3.7.6/hg38-graph-based/HG00096/ .

vcf="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/data/dragen-3.7.6/hg38-graph-based/HG00096/HG00096.hard-filtered.vcf.gz"
regions="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/custom_genes.bed"
# Note that tabix produces something that is no longer compressed.
tabix ${vcf} --regions ${regions} --separate-regions > "/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data/HG00096.hard-filtered.sliced.vcf"