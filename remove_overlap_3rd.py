import os
import subprocess
import sys
from Bio import pairwise2 as pw2

def calculate_seq_similarity(sgRNA_seq, adapter_seq):
	global_align = pw2.align.globalxx(adapter_seq, sgRNA_seq)
	matches = global_align[0][2]
	adapter_seq_length = global_align[0][4]
	return matches/adapter_seq_length

def main():
	dense_sgrna = sys.argv[1]
	even_sgrna = sys.argv[2]
	distance = sys.argv[3]
	adapter_seq = sys.argv[4]
	merge_dense_sgrna_file = dense_sgrna + ".merged"
	cmd = "sort -k1,1 -k2,2n %s|mergeBed -i stdin -c 4 -o collapse -d %d > %s" %(dense_sgrna, int(distance), merge_dense_sgrna_file)
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
	(output, _) = process.communicate() 
	out = open(even_sgrna, "w")
	for line in open(merge_dense_sgrna_file):
                cols = line.rstrip().split("\t")
                merged_sgrna_list = cols[3].split(",")
                potential_sgrna = merged_sgrna_list[0]
                if len(merged_sgrna_list) == 1:
                	###no overlap with other sgRNA
                	p_list = potential_sgrna.split("_")
                	sgRNA_seq = p_list[4]
                	adapter_seq_similarity = calculate_seq_similarity(sgRNA_seq, adapter_seq) ###add percentage of sequence similarity with adpter seq
                	out.write("%s\t%s\t%s\t%s\t%s\t%s\t%.2f\n" %(p_list[0], p_list[1],  p_list[2], potential_sgrna, "800", p_list[3], adapter_seq_similarity))
                	continue
                else:
                	p_list = potential_sgrna.split("_")
                	sgRNA_seq = p_list[4]
                	adapter_seq_similarity = calculate_seq_similarity(sgRNA_seq, adapter_seq) ###add percentage of sequence similarity with adpter seq
                	out.write("%s\t%s\t%s\t%s\t%s\t%s\t%.2f\n" %(p_list[0], p_list[1],  p_list[2], potential_sgrna, "800", p_list[3], adapter_seq_similarity)) ###output the first sgRNA
                	compare_list = merged_sgrna_list[1:]
                	keep_sgrna_last = ""
                	for sg in compare_list:
                		p_list = potential_sgrna.split("_")
                		sg_list = sg.split("_")
                		if p_list[0] == sg_list[0] and (int(sg_list[1]) - int(p_list[2])) >= abs(int(distance)):
                			if potential_sgrna!=merged_sgrna_list[0]:
                				sgRNA_seq = p_list[4]
                				adapter_seq_similarity = calculate_seq_similarity(sgRNA_seq, adapter_seq) ###add percentage of sequence similarity with adpter seq
                				out.write("%s\t%s\t%s\t%s\t%s\t%s\t%.2f\n" %(p_list[0], p_list[1], p_list[2], potential_sgrna, "800", p_list[3], adapter_seq_similarity))
                			keep_sgrna_last = potential_sgrna
                			potential_sgrna = sg
                	
                	p_list = potential_sgrna.split("_")
                	if not keep_sgrna_last == "": 
                		keep_sgrna_last_list = keep_sgrna_last.split("_")
                		if p_list[0] == keep_sgrna_last_list[0] and (int(p_list[1]) - int(keep_sgrna_last_list[2])) >= abs(int(distance)):
                			sgRNA_seq = p_list[4]
                			adapter_seq_similarity = calculate_seq_similarity(sgRNA_seq, adapter_seq) ###add percentage of sequence similarity with adpter seq
                			out.write("%s\t%s\t%s\t%s\t%s\t%s\t%.2f\n" %(p_list[0], p_list[1], p_list[2], potential_sgrna, "800", p_list[3], adapter_seq_similarity))

                	#	###output the last one no matter whether the left distance with last sgRNA is > distance(bp)
                	#	out.write("%s\t%s\t%d\t%s\t%s\t%s\n" %(sg_list[0], sg_list[1], int(sg_list[1]) + len(sg_list[3]), sg_list, "800", sg_list[2]))

	out.close()	
	#os.popen("rm %s" %merge_dense_sgrna_file)

if __name__ == '__main__':
	main()
