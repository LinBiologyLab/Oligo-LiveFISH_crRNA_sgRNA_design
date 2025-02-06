#!/bin/bash

ml CUDA/12.1.1
#DIR=$1
#PIPELINE_DIR=$2
WORKING_DIR=$1
MODE=G
CAS_OFFINDER_DIR="./cas-offinder-linux"

mkdir -p "$WORKING_DIR/sgRNA_casoffinder_output"
#Run Cas-OFFinder:cas-offinder-linux $INPUT_FILE $MODE $OUTPUT_FILE

for file in "$WORKING_DIR/sgRNA_casoffinder_input"/*; do
	INPUT_FILE="$file"
	BASENAME=$(basename "$INPUT_FILE" "_input.txt")
	OUTPUT_FILE="$WORKING_DIR/sgRNA_casoffinder_output/${BASENAME}_output.txt"
	touch "$OUTPUT_FILE"
	"$CAS_OFFINDER_DIR" "$INPUT_FILE" "$MODE" "$OUTPUT_FILE"       
done                                                                   
                                                                       
                                                                       
                                                                       
                                                                       
                                                                       
