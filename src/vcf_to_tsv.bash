#!/usr/bin/env bash
# $1 is vcf input path prefix without a final /
# $2 is tsv output path prefix without a final /

# https://stackoverflow.com/questions/9612090/how-to-loop-through-file-names-returned-by-find
# https://unix.stackexchange.com/questions/12902/how-to-run-find-exec

find "${1}" -maxdepth 1 -mindepth 1 -type f -name "*.vcf" \
    -exec gatk VariantsToTable --variant {} --output {}.tsv \;


# echo "${#vcf_paths[@]}"
# for vcf_path in "${vcf_paths[@]}";
# do
#     tsv_name=$(basename -s ".gvcf" "${vcf_path}")

#     echo "vcf_path: ${vcf_path}"
#     echo "tsv: ${2}/${tsv_name}"
#     # gatk VariantsToTable \
#     #     --variant "${vcf_path}" \
#     #     --output "${2}/${tsv_name}" 
# done