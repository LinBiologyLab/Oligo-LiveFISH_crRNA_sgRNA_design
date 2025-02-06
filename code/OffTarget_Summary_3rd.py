import os
import sys

####go over all the off-target (<= 1 mismatches) to exam whether multiple off-targets have close interval distance (<2000bp)

casoff_input = sys.argv[1]
summary_output = sys.argv[2]

#shell_cmd = "awk '{OFS="\t"; print $2,$3,$1,$4,$5,$6}' %s |sort -k1,1 -k2,2n > %s" %(casoff_input, casoff_input)
#print shell_cmd
#os.popen(shell_cmd)
####original GCCTATAATCCCAGCTACTCNNN	chr5_KI270791v1_alt	40100	GCCTgTAATCCCAGCTACTtGGG	-	2
###chr1	639944	GCCTATAATCCCAGCTACTCNNN	aCCTATAATCCCAGCTACTtGGG	-	2
pre_chrom = ""
pre_sgrna = ""
sgrna_list = []
start_list = []
offtarget_seq_list =[]
strand_list = []
mismatch_list = []
out = open(summary_output, "w")
for line in open(casoff_input):
	cols = line.rstrip().split("\t")
	#print line
	if pre_chrom == "":
		pre_sgrna = cols[2]
		pre_chrom = cols[0]
		sgrna_list.append(cols[2])
		start_list.append(int(cols[1]))
		offtarget_seq_list.append(cols[3])
		strand_list.append(cols[4])
		mismatch_list.append(cols[5])
	else:
		#print "000",start_list[-1]
		#print "111",int(cols[1])
		#print "abs",abs(int(start_list[-1]) - int(cols[1]))
		#if pre_sgrna == cols[2] and pre_chrom == cols[0] and (abs(int(start_list[-1]) - int(cols[1])) <2000):
				###consider multiple sgRNA off-target; interval distance increase to 20000
		if pre_chrom == cols[0] and abs(int(start_list[-1]) - int(cols[1])) <2000:
			sgrna_list.append(cols[2])
			start_list.append(int(cols[1]))
			offtarget_seq_list.append(cols[3])
			strand_list.append(cols[4])
			mismatch_list.append(cols[5])
		else:
			###output
			offtarget_seq_number = len(start_list)
			start_min = min(start_list)
			start_max = max(start_list)
			#out.write("%s\t%s\t%d\t%d\t%d\t%d\t%s\t%s\t%s\n" %(pre_sgrna, pre_chrom, start_min, start_max, start_max-start_min, offtarget_seq_number, ";".join(offtarget_seq_list), ";".join(strand_list), ";".join(mismatch_list)))
			out.write("%s\t%s\t%d\t%d\t%d\t%d\t%s\t%s\t%s\t%s\n" %(";".join(sgrna_list), pre_chrom, start_min, start_max, start_max-start_min, offtarget_seq_number, ";".join(offtarget_seq_list), ";".join(strand_list), ";".join(mismatch_list), ";".join(list(set(sgrna_list)))))
			###update record
			#print cols
			pre_sgrna = cols[2]
			pre_chrom = cols[0]
			sgrna_list = []
			start_list = []
			offtarget_seq_list = []
			strand_list = [] 
			mismatch_list = []
			sgrna_list.append(cols[2])
			start_list.append(int(cols[1]))
			offtarget_seq_list.append(cols[3])
			strand_list.append(cols[4])
			mismatch_list.append(cols[5])
		#print start_list, min(start_list), max(start_list)
out.close()
				
			
		

