import os
import sys

ori_site_file = sys.argv[1]
offtarget_site_file = sys.argv[2]
output_file = sys.argv[3]

ori_site_dict={} ###{seq: chr_start}
for line in open(ori_site_file):
	cols = line.rstrip().split("\t")
	sgrna = cols[3]
	#site = cols[0]+cols[1]
	ori_site_dict[sgrna] = [cols[0], cols[1], cols[5]] ## chrom, start, strand

out = open(output_file,"w")
for line in open(offtarget_site_file):
	cols = line.rstrip().split("\t")
	sgrna = cols[2][:-3]
	#offsite = cols[1]+cols[2]
	if int(cols[5]) > 0: 
		out.write(line)
	else:
		if sgrna in ori_site_dict.keys() and cols[4] == "+":
			if cols[0]==ori_site_dict[sgrna][0] and int(cols[1])==int(ori_site_dict[sgrna][1]):
				print ("OrisgRNA", line, ori_site_dict[sgrna])
		#elif cols[0]==ori_site_dict[sgrna][0] and abs(int(cols[1])-int(ori_site_dict[sgrna][1]))==1:
		#	print "OrisgRNA which adding G", line, ori_site_dict[sgrna]
			else:
				out.write(line)
		elif sgrna in ori_site_dict.keys() and cols[4] == "-":
			if cols[0]==ori_site_dict[sgrna][0] and (int(ori_site_dict[sgrna][1])-int(cols[1]))==3:
				print ("OrisgRNA", line, ori_site_dict[sgrna])
			else:
				out.write(line)
		else:
			out.write(line)

out.close()
