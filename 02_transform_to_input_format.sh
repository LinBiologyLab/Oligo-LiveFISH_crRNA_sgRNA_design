#!/bin/bash

#transform sgRNA into Cas-Offinder input format
#13~15bp mismatch=1, >=16bp mismatch=2
#DIR=$1
#PIPELINE_DIR=$2
WORKING_DIR=$1
GUIDE_LEN_MIN=$2
GUIDE_LEN_MAX=$3
sgRNA_col=4
INPUT_FILE=$4
BASENAME=$5
mkdir -p "$WORKING_DIR/sgRNA_casoffinder_input"

for length in $(seq $GUIDE_LEN_MIN $GUIDE_LEN_MAX); do
	output_file="$WORKING_DIR/sgRNA_casoffinder_input/${BASENAME}_${length}bp_input.txt"
	echo "./hg38.fa" > "$output_file"
	echo "$(printf '%.0sN' $(seq 1 $length))NGG" >> "$output_file"
	awk -v col="$sgRNA_col" -v len="$length" -v output_file="$output_file" '
	BEGIN { count=1 }
	length($col) == len { 
		if ( len >= 16) {
			print $col "NNN 2 Seq" count >> output_file
		} else {
			print $col "NNN 1 Seq" count >> output_file
		}	j
		count++
	}
	' "$INPUT_FILE"
done
