#!/usr/bin/env bash
# $1 is input
# $2 is output
sort -V -k1,1 -k2,2 -k3,3 --output ${2} ${1}