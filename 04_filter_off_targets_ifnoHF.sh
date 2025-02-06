#!/bin/bash

#DIR=$1
#PIPELINE_DIR=$2
WORKING_DIR=$1
BASENAME=$2
sgRNA_output_file="$3.bed"
INPUT_DIR="$WORKING_DIR/sgRNA_casoffinder_output"
PARENT_DIR=$(dirname "${WORKING_DIR}")

mkdir -p "$WORKING_DIR/offtarget_sorted_NoOri"
for file in "$INPUT_DIR"/*; 
do 
	INPUT_FILE="$file"
	FILE_NAME=$(basename "${INPUT_FILE%.txt}")
	tmpfile=$(mktemp "$WORKING_DIR/tmpfile.XXXXXX")
	if [[ "$FILE_NAME" == *"18"* ]]; then
		awk '{ OFS = "\t"; if ($6<2 && NF==6) print $2,$3,$1,$4,$5,$6}' $INPUT_FILE | grep chr3_KI.*alt -v | sort -k1,1 -k2,2n > "$tmpfile"
	else
		awk '{OFS="\t"; if(NF==6) print $2,$3,$1,$4,$5,$6}' $INPUT_FILE|grep chr3_KI.*alt -v |sort -k1,1 -k2,2n > "$tmpfile"
	fi 
	OUTPUT_FILE="$WORKING_DIR/offtarget_sorted_NoOri/${FILE_NAME}_sorted_NoOri_sgRNA.txt"
	python Remove_Original_TargetSites.py $sgRNA_output_file "$tmpfile" $OUTPUT_FILE
	rm -f "$tmpfile"                                    
done                                                        
                                                            
cat $WORKING_DIR/offtarget_sorted_NoOri/* |sort -k1,1 -k2,2n > "$WORKING_DIR"/${BASENAME}_Offtarget_sorted_NoOri_sgRNA.txt
python OffTarget_Summary_3rd.py "$WORKING_DIR/${BASENAME}_Offtarget_sorted_NoOri_sgRNA.txt" "$WORKING_DIR/${BASENAME}_Offtarget_summary_NoOri.txt"                                                        
awk '{split($1,a,";"); if($6>=2) {for(i=1;i<=length(a);i++) {print a[i]}}}' "$WORKING_DIR/${BASENAME}_Offtarget_summary_NoOri.txt" |sort|uniq -c > "$WORKING_DIR"/${BASENAME}_NoOri_sgRNA_2Sites_frequency.txt
                                                            
python Remove_HighPresent_sgRNA.py "$WORKING_DIR"/${BASENAME}_NoOri_sgRNA_2Sites_frequency.txt 100 "$WORKING_DIR"/${BASENAME}_Offtarget_sorted_NoOri_sgRNA.txt "$WORKING_DIR"/${BASENAME}_Offtarget_sorted_NoOri_NoHF_sgRNA.txt
python "$PIPELINE_DIR"/OffTarget_Summary_3rd.py "$WORKING_DIR/${BASENAME}_Offtarget_sorted_NoOri_NoHF_sgRNA.txt" "$WORKING_DIR/${BASENAME}_Offtarget_summary_NoOri_NoHF.txt"

#if no HF, will return 0
awk '$1>100' "$WORKING_DIR"/${BASENAME}_NoOri_sgRNA_2Sites_frequency.txt | sed -e 's/NNN$//'|awk '{OFS="\t"; print $2,$2}' > "$WORKING_DIR"/${BASENAME}_HF_2sgRNAFrequency.txt

if [ -s "$WORKING_DIR/${BASENAME}_HF_2sgRNAFrequency.txt" ]; then 
	python two_file_merge.py "$sgRNA_output_file" 4 "$WORKING_DIR"/${BASENAME}_HF_2sgRNAFrequency.txt 1 "$WORKING_DIR"/${BASENAME}_merge_possible_guide_2sgRNAFreq_output.txt
	grep nan "$WORKING_DIR"/${BASENAME}_merge_possible_guide_2sgRNAFreq_output.txt | cut -f 1 > "$WORKING_DIR"/${BASENAME}_18_20bp_WithG_NosgRNAFrequency_sgRNA.txt                                                    
	python two_file_merge.py "$WORKING_DIR"/${BASENAME}_18_20bp_WithG_NosgRNAFrequency_sgRNA.txt 1 "$sgRNA_output_file" 4 "$WORKING_DIR"/${BASENAME}_WithG_NOsgRNAFrequency_sgRNA.bed
else
	echo "No HF."
	cat "$sgRNA_output_file" > "$WORKING_DIR"/${BASENAME}_WithG_NOsgRNAFrequency_sgRNA.bed
fi	
                                                            
