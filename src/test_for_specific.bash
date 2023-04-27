#!/usr/bin/env bash

regions="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/custom_genes.bed"
start_of_local_path_to_sync="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/dragen-3.7.6/hg38-graph-based/"
local_path_for_transformed="/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data/"
# https://questhenkart.medium.com/looping-through-an-s3-bucket-and-performing-actions-using-the-aws-cli-and-bash-61394a91af89
# Note that origin has a trailing slash because aws s3 likes that.
origin="s3://1000genomes-dragen/data/dragen-3.7.6/hg38-graph-based/"
for remote_end_of_path in $(aws s3 ls --no-sign-request "${origin}");
do
    # Sometimes we have text that says PRE,
    # but we don't like that.
    if [ "${remote_end_of_path}" != "PRE" ] && [ "${remote_end_of_path}" = "HG002/" ];
    then
        echo "in if"
        # remote_end_of_path will not have PRE
        local_path_to_sync="${start_of_local_path_to_sync}${remote_end_of_path}"
        mkdir -p "${local_path_to_sync}"
        
        # Download.
        # Notice here that unlike the main loop,
        # the directory here of ${origin}${remote_end_of_path}
        # is more specific.
        aws s3 sync \
            --no-sign-request \
            --exclude="*" \
            --include="*.hard-filtered.vcf.gz*" \
            ${origin}${remote_end_of_path} "${local_path_to_sync}" 
        
        # Check download.
        # Currently, this isn't working because the files *.md5sum
        # do not have the filenames in them.
        # md5sum -c "${local_path_to_sync}*.md5sum"

        vcf="${local_path_to_sync}*.vcf.gz"
        vcf_basename=$(basename -s ".vcf.gz" ${vcf})
        # Note that tabix produces something that is no longer compressed.
        echo "about to run tabix"
        echo "vcf: ${vcf}"
        echo "regions: ${regions}"
        echo "local_path_for_transformed: ${local_path_for_transformed}"
        tabix ${vcf} --regions ${regions} --print-header > "${local_path_for_transformed}${vcf_basename}.sliced.with_header_2.vcf"
        # Clean-up
        # gzip "${local_path_for_transformed}vcf_basename.sliced.vcf"
        rm -r -f "${local_path_to_sync}"
    fi 
done