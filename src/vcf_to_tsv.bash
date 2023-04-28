#!/usr/bin/env bash
# $1 is vcf input path
# $2 is tsv output path
gatk VariantsToTable \
    --variant "${1}" \
    --output "${2}" 