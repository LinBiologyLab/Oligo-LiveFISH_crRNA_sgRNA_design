#!/bin/bash
BEDF=$1
GUIDE_LEN_MIN=18
GUIDE_LEN_MAX=20

#STEP1: run generate_possible_guides.py
basename=$(basename $BEDF .bed)
mkdir -p "./result_region_dir/${basename}"
WORKING_DIR="./result_region_dir/${basename}"
sgRNA_output_file=$WORKING_DIR/possible_sgRNA_${basename}_${GUIDE_LEN_MIN}_${GUIDE_LEN_MAX}bp
#bash 01_run_generate_possible_guides.sh $WORKING_DIR $BEDF $GUIDE_LEN_MAX $GUIDE_LEN_MIN $sgRNA_output_file 


#STEP2:transfrom possible sgRNA to cas-offinder input format
#>=16bp mismatch=2
#bash 02_transform_to_input_format.sh $WORKING_DIR $GUIDE_LEN_MIN $GUIDE_LEN_MAX "${sgRNA_output_file}.txt" $basename

#STEP3:run cas-offinder
#bash 03_run_cas_offinder.sh $WORKING_DIR 

#STEP4:filter off targets
#bash 04_filter_off_targets_ifnoHF.sh $WORKING_DIR $basename $sgRNA_output_file	

#STEP5:remove offtargets and generate final sgRNA candidates
bash 05_remove_sgRNA_offtarget_2_10_sites_tmp.sh $WORKING_DIR $basename
	

