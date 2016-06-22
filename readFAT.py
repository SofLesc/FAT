#!/usr/bin/python
import sys
import getopt
import os

def main(argv):
	
	directory = 'readtest'
	input_name = ''
	# 300 = 100 caracteres
	cluster_size = 300
	ofset = 300
	
	try:
		opts, args = getopt.getopt(argv,"hi:",["input_name"])
	except getopt.GetoptError:
		print 'createFAT.py -d <directory>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'readFAT.py -i <input>'
			sys.exit()
		elif opt in ("-i", "--input_name"):
			input_name = arg
	input_file = open(input_name)	
	
	os.mkdir(directory, 0755)
	os.chdir(directory)
	
	file_name = ''	
	count = 0
	first = 1
	number_of_files = 0
	file_number = 0

	for line in input_file:
		count = count + 1
		if(first):
			count = 0
			first = 0
			number_of_files = int(line)
		else:
			if line != '20\n' and count < 9:
				file_name = file_name + line[0:-1].decode('hex')
			if count == 9:
				file_name = file_name + '.'
			#File extension		
			if count >= 9 and count < 12:
				file_name = file_name + line[0:-1].decode('hex')
			if count == 11:	
				print file_name	
				new_file = open(file_name, "w")
				file_name = ''
			if count == 12:
				 cluster = int(line)
			if count == 13:
				count = 0
				size = int(line)
				#data
				input_file.seek(ofset + cluster*cluster_size)
				line_number = 1	
				content = ''		
				for line in input_file:
					if line_number > size:
						break
					content = content + line[0:-1].decode('hex')
					line_number = line_number + 1
				input_file.seek((cluster + 1)*14*3)
				new_file.write(content)
				file_number = file_number + 1
				if(file_number == number_of_files):
					break

if __name__ == "__main__":
   main(sys.argv[1:])
