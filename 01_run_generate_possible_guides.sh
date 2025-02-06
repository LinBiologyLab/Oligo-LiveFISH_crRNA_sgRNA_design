#!/bin/bash

ml Biopython/1.78-foss-2020b-Python-3.8.6
ml BEDTools
#DIR=$1
#PIPELINE_DIR=$2
WORKING_DIR=$1
input_bed=$2
GUIDE_LEN_MAX=$3
GUIDE_LEN_MIN=$4
OUTPUT=$5

python generate_possible_guides.py $input_bed hg38.fa GG $GUIDE_LEN_MAX $GUIDE_LEN_MIN 0.35 0.8 $OUTPUT
