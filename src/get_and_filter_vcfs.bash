#!/usr/bin/env bash

local_path_to_sync="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/data/dragen-3.7.6/hg38-graph-based"
# https://questhenkart.medium.com/looping-through-an-s3-bucket-and-performing-actions-using-the-aws-cli-and-bash-61394a91af89
# Note that origin has a trailing slash because aws s3 likes that.
origin="s3://1000genomes-dragen/data/dragen-3.7.6/hg38-graph-based/"
for remote_path in $(aws s3 ls --no-sign-request "${origin}");
do
    # Sometimes we have text that says PRE,
    # but we don't like that.
    if [[ "${remote_path}" != "PRE" ]];
    then
        # modified_remote_path will not have PRE
        modified_remote_path="${remote_path}"

        aws s3 sync \
            --no-sign-request \
            --exclude="*" \
            --include="*.hard-filtered.vcf.gz*" \
            ${origin}${modified_remote_path} "${local_path_to_sync}"
    fi

    
done



# vcf="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/data/dragen-3.7.6/hg38-graph-based/HG00096/HG00096.hard-filtered.vcf.gz"
# regions="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/custom_genes.bed"
# # Note that tabix produces something that is no longer compressed.
# tabix ${vcf} --regions ${regions} --separate-regions > "/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data/HG00096.hard-filtered.sliced.vcf"