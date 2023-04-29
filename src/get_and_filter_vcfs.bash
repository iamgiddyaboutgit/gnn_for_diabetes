#!/usr/bin/env bash

# Change these 3 variable paths according to your system.
regions="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/pathway_data/custom_genes.bed"
start_of_local_path_to_sync="/home/jpatterson87/for_classes/gnn_for_diabetes/data/raw_data/dragen-3.7.6/hg38-graph-based/"
local_path_for_transformed="/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data/"

# https://questhenkart.medium.com/looping-through-an-s3-bucket-and-performing-actions-using-the-aws-cli-and-bash-61394a91af89
# Note that origin has a trailing slash because aws s3 likes that.
origin="s3://1000genomes-dragen/data/dragen-3.7.6/hg38-graph-based/"
for remote_end_of_path in $(aws s3 ls --no-sign-request "${origin}");
do

    first_two_chars_of_remote_end_of_path=$(echo "${remote_end_of_path}" | cut -c 1-2 -)
    if [[ "${first_two_chars_of_remote_end_of_path}" == "HG" ]] || [[ "${first_two_chars_of_remote_end_of_path}" == "NA" ]];
    then
        local_path_to_sync="${start_of_local_path_to_sync}${remote_end_of_path}"

        # A Bash-ism is used here to remove a trailing /
        gvcf_basename="${remote_end_of_path%/}.hard-filtered"
        transformed_gvcf="${local_path_for_transformed}${gvcf_basename}.sliced.gvcf"
        # Ok, but have we already downloaded the files?
        if [[ ! -f "${transformed_gvcf}" ]];
        then
            # We have not already downloaded the files.
            mkdir -p "${local_path_to_sync}"
            # Download.
            # Notice here that unlike the main loop,
            # the directory here of ${origin}${remote_end_of_path}
            # is more specific.

            aws s3 sync \
                --no-sign-request \
                --exclude="*" \
                --include="*.hard-filtered.gvcf.gz*" \
                ${origin}${remote_end_of_path} "${local_path_to_sync}" 
            
            # Check download.
            # Currently, this isn't working because the files *.md5sum
            # do not have the filenames in them.
            # md5sum -c "${local_path_to_sync}*.md5sum"
            
            # Note that tabix produces something that is no longer compressed.
            gvcf=${local_path_to_sync}${gvcf_basename}.gvcf.gz
            echo "running tabix on ${gvcf}"
            # --separate-regions  is another option that can be used for tabix
            tabix ${gvcf} --regions ${regions} --print-header > "${local_path_for_transformed}${gvcf_basename}.sliced.gvcf"
            
            # Clean-up
            # gzip "${local_path_for_transformed}gvcf_basename.sliced.gvcf"
            echo "cleaning up for the next iteration"
            rm -r -f "${local_path_to_sync}" 
        fi 
    fi 
done

