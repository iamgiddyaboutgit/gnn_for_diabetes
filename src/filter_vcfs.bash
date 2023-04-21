#!/usr/bin/env bash

vcf="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/data/dragen-3.7.6/hg38-graph-based/HG00096/HG00096.hard-filtered.vcf.gz"
regions="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/custom_genes.bed"
tabix ${vcf} --regions ${regions}