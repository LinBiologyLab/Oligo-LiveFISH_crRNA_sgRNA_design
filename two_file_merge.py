import os
import sys
'''
python two_file_merge.py 1st_file 2st_file out_file
1st_file offer a sort list
2st_file have a list corresponding (1st col) to 1st and other information
generate sort 2st_file
'''
#if len(sys.argv) != 6:
#	print "python two_file_merge.py 1st_file ref_col 2st_file match_col out_file"
#	exit()
sort_list_file = sys.argv[1]
sort_select_col = int(sys.argv[2]) - 1
sorted_file = sys.argv[3]
sorted_col = int(sys.argv[4]) - 1
out_file = sys.argv[5]

if len(sys.argv)>6:
	action = sys.argv[6]
else:
	action = "Keep"


out = open(out_file, 'w')
info_dict = {}   

for line in open(sorted_file):
	if line.startswith("#"):
		continue
	key = line.rstrip().split('\t')[sorted_col].upper()
	#print key
	#key = line.rstrip().split('\t')[sorted_col].split(".")[0]
	#key = line.rstrip().split()[sorted_col]
	if key in info_dict:
		#print key,line
		#print "Warning: redundant element in second file"
		info_dict[key].append(line)
	else:
		info_dict[key] = []
		#info_dict[key] = line
		info_dict[key].append(line)
col_numbers = len(line.rstrip().split('\t'))
nofind_num=0
for ori_line in open(sort_list_file):
	#print (key)
	#key = line.rstrip().split("\t")[sort_select_col]
	#print (ori_line.rstrip().split())
	key = ori_line.rstrip().split()[sort_select_col].upper()
	if key in info_dict:
		#for line in info_dict[key]:
		#	out.write("%s\t%s\n" %(line.rstrip(), ori_line.rstrip()))
		out.write(info_dict[key][0])
	else:
		print (key)
		nofind_num +=1
		if action == "Keep":
			out.write("%s" %(key))
			for i in range(1,col_numbers):
				out.write("\t%s" %"nan")
			out.write("\t%s" %"nan")
			out.write("\n")
out.close()
print ('can\'t find %d element' %nofind_num)
