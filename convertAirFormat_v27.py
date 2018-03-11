# -*- coding: utf-8 -*-
"""
$sudo easy_install pip
$sudo pip install xlrd
to convert a specific data type
"""

import sys
import glob,os
import xlrd	# -- to directly open xls file

if __name__ == "__main__":

	infile_dir = sys.argv[1]	# -- testFolder
	os.chdir(infile_dir)
	for infile_name in glob.glob("*.xls"): #= sys.argv[1]  # -- src = r"/Users/wychung/Downloads/formatTest.xls"
		print infile_dir, infile_name

		outfile_name = infile_name.split('.')[0]+'.txt'
		outfile = open(outfile_name,'w')
	
		book = xlrd.open_workbook(infile_name)
		work_sheet = book.sheet_by_index(0)

		current_row = 1
		num_rows = work_sheet.nrows

		while current_row < num_rows:
			for j in range(24):
				outfile.write(work_sheet.cell_value(current_row,0)+'/'+str(j)+',')
				outfile.write(work_sheet.cell_value(current_row,1).encode('utf-8')+',')
				outfile.write(work_sheet.cell_value(current_row,2).encode('utf-8')+',')
				outfile.write(str(work_sheet.cell_value(current_row,j+3)))
				outfile.write('\n')
			current_row += 1

		outfile.close()

	"""
	for i, line in enumerate(file(infile_name)):
		line = line.rstrip()
		fields = line.split(',')
	
		if i > 0:
			for j in range(24):
				print fields[0]+'/'+str(j),fields[1],fields[2],fields[j+3]
		else:
			print line
	"""
