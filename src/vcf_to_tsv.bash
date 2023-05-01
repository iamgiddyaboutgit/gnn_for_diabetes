#!/usr/bin/env bash
# $1 is vcf input path prefix without a final /
# $2 is tsv output path prefix without a final /

vcf_paths=$(find "${1}" -maxdepth 1 -mindepth 1 -type f -name "*.vcf" -print0)

for vcf_path in "${vcf_paths}";
do
    tsv_name=$(basename -s ".vcf" "${vcf_path}")

    # gatk VariantsToTable \
    #     --variant "${vcf_path}" \
    #     --output "${2}/${tsv_name}" 
done