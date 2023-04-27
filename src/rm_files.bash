#!/usr/bin/env bash

na_files=$(find /home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data -name "NA*")

for na_file in "${na_files}";
do
    first_char=$(head -n 1 "${na_file}" | cut -c 1-1 -)
    if [[ "${first_char}" != "#" ]];
    then
        rm ${na_file}
    fi
done

hg_files=$(find /home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data -name "HG*")

for hg_file in "${hg_files}";
do
    first_char=$(head -n 1 "${hg_file}" | cut -c 1-1 -)
    if [[ "${first_char}" != "#" ]];
    then
        rm ${hg_file}
    fi
done