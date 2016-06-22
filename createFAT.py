#!/usr/bin/python
import sys
import getopt
import os

def main(argv):
	
	directory = ''
	output = 'output.txt'
	output_file = open(output, "w")
	cluster = 0
	# 300 = 100 caracteres
	cluster_size = 300
	ofset = 300
	
	try:
		opts, args = getopt.getopt(argv,"hd:",["directory"])
	except getopt.GetoptError:
		print 'createFAT.py -d <directory>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'createFAT.py -d <directory>'
			sys.exit()
		elif opt in ("-d", "--directory"):
			directory = arg
	print 'Directory is', directory
	
	#Deixa espaco para escrever no arquivo	
	for i in range(1000):		
		output_file.write('  \n')
	output_file.seek(0)	
	
	number_of_files = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
	output_file.write("%02d" % (number_of_files,) + '\n')
		

	for filename in os.listdir(directory):
		count = 0
		for c in filename:
			if hex(ord(c)) != '0x2e':
				output_file.write(c.encode("hex") +'\n')
				count = count + 1
			else:
				diff = 8 - count
				for i in range(diff):
					output_file.write('20\n')
		output_file.write("%02d" % (cluster,) + '\n')
		#output_file.seek(ofset + cluster*cluster_size)
		output_file.seek(ofset + cluster*cluster_size)
		current_file = open(directory + '/' + filename)
		size = 0		
		for line in current_file:
			for c in line:
				output_file.write(c.encode("hex") +'\n')
				size = size + 1	
		cluster = cluster + 1
		output_file.seek(cluster*13*3)
		output_file.write("%02d" % (size,) + '\n')
			
			
if __name__ == "__main__":
   main(sys.argv[1:])
