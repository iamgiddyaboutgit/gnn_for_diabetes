#!/usr/bin/env bash

# https://stackoverflow.com/questions/9612090/how-to-loop-through-file-names-returned-by-find
# https://unix.stackexchange.com/questions/12902/how-to-run-find-exec
vcf_input="/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data_from_vms"
tsv_input="/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data_from_vms"
src_dir="/home/jpatterson87/for_classes/gnn_for_diabetes/src"
output_dir="/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data_from_vms/with_nodes"

# find "${vcf_input}" -maxdepth 1 -mindepth 1 -type f -name "*.vcf" \
#     -exec gatk VariantsToTable --variant {} --output {}.tsv \;

for vcf in ${vcf_input}/*.vcf; do 
    cut -f 1,2,4,5 "${vcf}" > "${vcf}.cut"
done

"${src_dir}"/add_nodes_to_tsv.py \
    --tsv "${tsv_input}" \
    --vcf "${vcf_input}" \
    -o "${output_dir}"
