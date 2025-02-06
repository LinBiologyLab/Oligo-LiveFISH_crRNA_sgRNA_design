import os
import sys

frequency_summary_inf = sys.argv[1]
hf_cutoff = int(sys.argv[2])
casoff_output = sys.argv[3]
filter_output = sys.argv[4]

hf_sgrna = []
for line in open(frequency_summary_inf):
	cols = line.rstrip().split()
	frequency = cols[0]
	sgrna = cols[1]
	if int(frequency) > hf_cutoff:
		hf_sgrna.append(sgrna)
print (len(hf_sgrna))

out = open(filter_output, "w")
for line in open(casoff_output):
	cols = line.rstrip().split("\t")
	sgrna = cols[2]
	if sgrna in hf_sgrna:
		continue
	else:
		out.write(line)
out.close()
