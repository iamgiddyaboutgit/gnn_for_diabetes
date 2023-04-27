#!/usr/bin/env bash

regions="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/custom_genes.bed"
start_of_local_path_to_sync="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/dragen-3.7.6/hg38-graph-based/"
local_path_for_transformed="/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data/"
# https://questhenkart.medium.com/looping-through-an-s3-bucket-and-performing-actions-using-the-aws-cli-and-bash-61394a91af89
# Note that origin has a trailing slash because aws s3 likes that.
origin="s3://1000genomes-dragen/data/dragen-3.7.6/hg38-graph-based/"
for remote_end_of_path in $(aws s3 ls --no-sign-request "${origin}");
do
    local_path_to_sync="${start_of_local_path_to_sync}${remote_end_of_path}"
    vcf="${local_path_to_sync}*.vcf.gz"
    vcf_basename=$(basename -s ".vcf.gz" ${vcf})
    # Sometimes we have text that says PRE,
    # but we don't like that.
    # Also, sometimes we have already downloaded the needed files.
    if [[ "${remote_end_of_path}" != "PRE" ]] && [[ ! -f "${local_path_for_transformed}${vcf_basename}.sliced.vcf"]];
    then
        # remote_end_of_path will not have PRE
        # transformed data will not have been written yet.
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
        
        # Note that tabix produces something that is no longer compressed.
        echo "running tabix"
        tabix ${vcf} --regions ${regions} --print-header > "${local_path_for_transformed}${vcf_basename}.sliced.vcf"
        # Clean-up
        # gzip "${local_path_for_transformed}vcf_basename.sliced.vcf"
        echo "cleaning up for the next iteration"
        rm -r -f "${local_path_to_sync}"       
    fi 
done

