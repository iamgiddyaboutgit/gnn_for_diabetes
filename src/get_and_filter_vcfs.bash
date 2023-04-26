#!/usr/bin/env bash

local_path_to_sync="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/data/dragen-3.7.6/hg38-graph-based"
# https://questhenkart.medium.com/looping-through-an-s3-bucket-and-performing-actions-using-the-aws-cli-and-bash-61394a91af89
origin="s3://1000genomes-dragen/data/dragen-3.7.6/hg38-graph-based/"
for remote_path in $(aws s3 ls --no-sign-request "${origin}");
do
    # Bash-ism that removes trailing slash
    modified_remote_path=${remote_path%/}
    # Sometimes we have text that says PRE,
    # but we don't like that.
    if [[ "${modified_remote_path}" != "PRE" ]];
    then
        # double_modified_remote_path will not have PRE
        double_modified_remote_path="${modified_remote_path}"

done
# aws s3 sync \
#     --no-sign-request \
#     --exclude="*" \
#     --include="*.hard-filtered.vcf.gz*" \
#     s3://1000genomes-dragen/data/dragen-3.7.6/hg38-graph-based/ "${path_to_sync}"

# vcf="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/data/dragen-3.7.6/hg38-graph-based/HG00096/HG00096.hard-filtered.vcf.gz"
# regions="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/custom_genes.bed"
# # Note that tabix produces something that is no longer compressed.
# tabix ${vcf} --regions ${regions} --separate-regions > "/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data/HG00096.hard-filtered.sliced.vcf"