#!/bin/bash
ml Biopython/1.78-foss-2020b-Python-3.8.6
ml BEDTools
WORKING_DIR=$1
BASENAME=$2
mkdir -p "$WORKING_DIR/sgRNA_NoOfftarget_2_10_sitesinregion"
OUTPUT_DIR="$WORKING_DIR/sgRNA_NoOfftarget_2_10_sitesinregion"

#offtarget region with >=2-10 offtarget sites

for i in 2
do
#	echo "$i"
	temp1=$(mktemp -p "$WORKING_DIR")
	temp2=$(mktemp -p "$WORKING_DIR")
	temp3=$(mktemp -p "$WORKING_DIR")
	awk -v site="$i" '{split($1,a,";"); if($6>=site) {for(j=1;j<=length(a);j++) {print a[j]}}}' $WORKING_DIR/${BASENAME}_Offtarget_summary_NoOri_NoHF.txt | sort | uniq | sed -e 's/NNN$//' | awk '{OFS="\t"; print $1,$1}' > "$temp1"
	cut -f 4 $WORKING_DIR/${BASENAME}_WithG_NOsgRNAFrequency_sgRNA.bed | cat - "$temp1" | cut -f 1|sort|uniq -c|awk '{if($1==1) print $2}' > "$temp2"
	python two_file_merge.py "$temp2" 1 "$WORKING_DIR/${BASENAME}_WithG_NOsgRNAFrequency_sgRNA.bed" 4 "$temp3"
	awk '{OFS="\t"; print $1,$2,$3,$1"_"$2"_"$3"_"$6"_"$4,".",$6}' "$temp3" | sort -k1,1 -k2,2n > "$OUTPUT_DIR/${BASENAME}_${i}SitesInRegion_sgRNA_NoOfftarget_new.bed"
	python remove_overlap_3rd.py "$OUTPUT_DIR/${BASENAME}_${i}SitesInRegion_sgRNA_NoOfftarget_new.bed" "$OUTPUT_DIR/${BASENAME}_${i}SitesInRegion_sgRNA_NoOfftarget_Spacer10.bed" 10 TGGTACGGGAACAGCAC
	rm "$temp1" "$temp2" "$temp3"
done
