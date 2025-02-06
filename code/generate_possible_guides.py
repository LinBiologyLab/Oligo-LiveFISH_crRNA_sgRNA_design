import os
import sys
from Bio.Seq import Seq
import string
import re
from Bio import pairwise2 as pw2

def calculate_GC_content(seq):
	return float(seq.count('C') + seq.count('G'))/len(seq)

def generate_sgRNA_seq(pam_index, strand, guide_len_max, guide_len_min, region_name, region_seq, gc_l, gc_u, out_bed, out_txt):
	region_chrom = region_name.split("(")[1].split(":")[0]
	region_start = int(region_name.split(":")[1].split("-")[0])
	for pi in pam_index:
		#for guide_len in range(guide_len_min, guide_len_max+1): 
		###revise 04172023
		for guide_len in range(guide_len_min, guide_len_max+1)[::-1]: 
			if strand == "+":
				sgRNA_seq_start = pi[0] - (guide_len+1)
				sgRNA_seq_end = pi[0] - 2
			else:
				sgRNA_seq_start = pi[1] + 1
				sgRNA_seq_end = pi[1] +  guide_len 
			if sgRNA_seq_start < 0 or sgRNA_seq_end >= (len(region_seq)-1):
				continue
			##retrive sgRNA seq
			sgRNA_seq = region_seq[sgRNA_seq_start:(sgRNA_seq_end+1)]
			if strand == "-":
				sgRNA_seq = str(Seq(sgRNA_seq).reverse_complement()) 
			#check whether the 1st bp in sgRNA seq is G. If not, next
			if sgRNA_seq[0] == "G": 
					break
			else:
					continue
		if sgRNA_seq_start < 0 or sgRNA_seq_end >= (len(region_seq)-1):
			continue
		if not sgRNA_seq[0] == "G": continue
		#filter sgRNA by specific sequences	
		#remove sgRNA contain special seq: TTTT; 10G; CTCGAG; GCTNAGC; CCANNNNNNTGG. The last three seqs are enzyme_cutting_seqs
		if re.findall("TTTT",sgRNA_seq): continue
		if re.findall("G{10}", sgRNA_seq): continue
		if re.findall("CTCGAG",sgRNA_seq): continue
		if re.findall("GCT.AGC",sgRNA_seq): continue
		if re.findall("CCA......TGG",sgRNA_seq): continue
		#filter sgRNA by gc_content
		sgRNA_seq_gc_content = calculate_GC_content(Seq(sgRNA_seq))
		if sgRNA_seq_gc_content < gc_l or sgRNA_seq_gc_content > gc_u:
			continue
		#region_sgRNA_dict[region_name].append([sgRNA_seq, sgRNA_seq_start, strand])
		#output each sgRNA seq; columns: chr; start; end; seq; region; strand ###bed: seq start with 0; txt: seq start wtih 1
		out_bed.write("%s\t%d\t%d\t%s\t%s\t%s\n" %(region_chrom,region_start+sgRNA_seq_start, region_start+sgRNA_seq_end+1,  sgRNA_seq, region_name, strand))
		out_txt.write("%s\t%d\t%d\t%s\t%s\t%s\n" %(region_chrom,region_start+sgRNA_seq_start+1, region_start+sgRNA_seq_end+1,  sgRNA_seq, region_name, strand))

def generate_all_sgRNA(region_seq, pam, guide_len_max, guide_len_min, gc_l, gc_u, out_name):
	out_bed = open(out_name + ".bed", "w")
	out_txt = open(out_name + ".txt", "w") ##start with 1; for genome browser
	pam_rc = str(Seq(pam).reverse_complement()) 
	#region_sgRNA_dict = {} ###key: region_name; value: [[seq, start,  strand],[]..]
	for line in open(region_seq):
		cols = line.rstrip().split("\t")
		region_name = cols[0] #KRAS_Enhancer_1(chr12:25099355-25100519) 
		print(line,region_name)
		region_seq = cols[1].upper()
		#region_sgRNA_dict[region_name] = []
		forward_pam_index =  [(m.start(0), m.end(0)) for m in re.finditer(pam, region_seq)] ###return [(2, 4), (11, 13), (15, 17)]
		reverse_pam_index =  [(m.start(0), m.end(0)) for m in re.finditer(pam_rc, region_seq)] ###return [(2, 4), (11, 13), (15, 17)]
		##go over all the pam and generate the sgRNA seq
		generate_sgRNA_seq(forward_pam_index, "+", guide_len_max, guide_len_min, region_name, region_seq, gc_l, gc_u, out_bed, out_txt)
		generate_sgRNA_seq(reverse_pam_index, "-", guide_len_max, guide_len_min, region_name, region_seq, gc_l, gc_u, out_bed, out_txt)
	out_bed.close()
	out_txt.close()

def main():
	###input: 
		#1.bed file contain region information; e.g. chr12	25402031	25405736	Promoter_KRAS; Note: no strand info here
		#2.fasta file with genome sequences; e.g. hg19.fa
		#3.PAM seq; e.g. SpCas9: NGG
		#4.length;
		#5.GC content lower cutoff; e.g. 0.35
		#6.GC content upper cutoff; e.g. 0.8
		#7.whether seq start with G, if not, add it
	###output: design possible guides in these regions
		#columns: chr; start; end; seq; region; strand ###seq start with 0
	bedf = sys.argv[1]
	ref_fa = sys.argv[2]
	pam = sys.argv[3]
	guide_len_max = int(sys.argv[4])
	guide_len_min = int(sys.argv[5])
	gc_l = float(sys.argv[6])
	gc_u = float(sys.argv[7])
	out_name = sys.argv[8]

	###use bedtools to retrieve sequence in bed region; only retrieve forward(+) sequences 
	region_seq = bedf[:-4] + "_seq.txt"
	p=os.popen("bedtools getfasta -fi %s -bed %s -fo %s -name -tab" %(ref_fa,bedf, region_seq ));p.close()
	###design candidate sgRNA with PAM and length second version!!!!
		#1. search PAM seq (GG+ or CC-)
		#2. retrieve sgRNA seq with defined length and PAM (GG+: upstream (length + 1)bp; CC-: downstream (length + 1)bp, then do reverse + complementary)
#3. the 1st bp should be G; Check from guide_len_max to guide_len_min, only select the biggist length started with G.  If not, remove it!!!
		#4. remove sgRNA contain special seq: TTTT; 10G; CTCGAG; GCTNAGC; CCANNNNNNTGG. The last three seqs are enzyme_cutting_seqs
		#5. check GC content
	generate_all_sgRNA(region_seq, pam, guide_len_max, guide_len_min, gc_l, gc_u, out_name)
		


if __name__=='__main__':
		    main()
