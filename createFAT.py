#!/usr/bin/python
import sys
import getopt
import os

output = 'output.txt'
output_file = open(output, "w")
cluster = 0
directory_number = 0
# 300 = 100 caracteres
cluster_size = 300
ofset = 300
file_number = 0

# Nome do arquivo em 8 bytes
# Extensao do arquivo em 3 bytes
# Cluster de dados em 1 byte (endereco dos dados) ou numero de pasta
# Tamanho do arquivo em 2 bytes
# Numero de pasta onde se encontra 2 bytes

#Exemplo
#n = numero de arquivo ou pasta
#p = parent directory
#    name               |   ext  |n | size| p
#74 65 73 74 20 20 20 20 74 78 74 00 00 05 00 00
#t  e  s  t  20 20 20 20 t  x  t  00 00 05 00 00

#70 61 73 74 61 20 20 20 20 20 20 01 00 00 00 00
#p  a  s  t  a  20 20 20 20 20 20 01 00 00 00 00

#Analisa as pastas e subpastas
def parseDirectory (directory, parentDirectory):
	global cluster
	global directory_number
	global file_number
	for filename in os.listdir(directory):
		count = 0
		if(os.path.isdir(directory + '/' + filename) == 1):
			for c in filename:
				output_file.write(c.encode("hex") +' ')
				#output_file.write(c +'  ')
			for i in range(11 - len(filename)):
				output_file.write('20 ')
			directory_number += 1
			output_file.write("%02d" % (directory_number,) + ' ')
			output_file.write('00 00 ')
			output_file.write('00 ')
			output_file.write("%02d" % (parentDirectory,) + '\n')
			print filename + " is a directory"
			file_number += 1
			os.chdir(directory)
			parseDirectory(filename, directory_number)
			os.chdir("..")
		else:
			print filename			
			for c in filename:
				if hex(ord(c)) != '0x2e':
					output_file.write(c.encode("hex") +' ')
					#output_file.write(c +'  ')
					count = count + 1
				else:
					diff = 8 - count
					for i in range(diff):
						output_file.write('20 ')
			output_file.write("%02d" % (cluster,) + ' ')
			output_file.seek(ofset + cluster*cluster_size)
			current_file = open(directory + '/' + filename)
			size = 0	
			#TODO copy in binary not hexa	
			for line in current_file:
				for c in line:
					output_file.write(c.encode("hex") +'\n')
					size = size + 1	
			output_file.seek(file_number*16*3 + 3*12)
			cluster = cluster + 1
			file_number += 1
			high = size/256
			output_file.write("%02x" % (high,) + ' ')
			low = size - 256*high
			output_file.write("%02x" % (low,) + ' ')
			output_file.write('00 ')
			output_file.write("%02d" % (parentDirectory,) + '\n')
			

def main(argv):
	
	directory = ''
	
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
	print 'Directory to analyse: ', directory
	
	#Deixa espaco para escrever no arquivo	
	for i in range(1000):		
		output_file.write('  \n')
	output_file.seek(0)	
	
	#number_of_files = len([name for name in os.listdir(directory)])
	#output_file.write("%02d" % (number_of_files,) + '\n')
		
	parseDirectory(directory, 00)
			
if __name__ == "__main__":
   main(sys.argv[1:])
