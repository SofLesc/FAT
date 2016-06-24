#!/usr/bin/python
import sys
import getopt
import os

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

def main(argv):
	
	directory = 'readtest'
	input_name = ''
	# 300 = 100 caracteres
	cluster_size = 300
	ofset = 300
	pastas = {}
	pastas[0] = directory
	
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
	
	if(os.path.isdir(directory) == 0):	
		os.mkdir(directory, 0755)
	#os.chdir(directory)
	
	file_name = ''	
	count = 0
	number_of_files = 0
	file_number = 0
	directory = False
	parent_directory = 0
	file_number = 0
	

	for line in input_file:
		start = 0
		end = 2
		first = True

		#File name
		for i in range (8):
			aux = int(line[start:end], 16)
			if(aux > 33):
				file_name = file_name + line[start:end].decode('hex')
			start +=3
			end += 3

		#File extension		
		for i in range (3):
			aux = int(line[start:end], 16)
			if(aux > 33):
				if(first):
					file_name += "."
					first = False
				file_name = file_name + line[start:end].decode('hex')
			else:
				directory = True
			start +=3
			end += 3
		print file_name
		if (directory):
			file_number += 1
			directory = False
			directory_number = int(line[start:end], 16)
			parent_directory = int(line[-3:-1], 16)
			os.mkdir(pastas[parent_directory] + "/" + file_name)
			pastas[directory_number] = pastas[parent_directory] + "/" + file_name
			file_name = ''
			continue
		else:
			file_number += 1
			parent_directory = int(line[-3:-1], 16)
			new_file = open(pastas[parent_directory] + "/" + file_name, "w")
			cluster = int(line[start:end], 16)
			start +=6
			end += 6
			# TODO Pegar os dois bits
			size = int(line[start:end], 16)
			file_name = ''
			input_file.seek(ofset + cluster*cluster_size)
			line_number = 1	
			content = ''		
			for line in input_file:
				if line_number > size:
					break
				content = content + line[0:-1].decode('hex')
				line_number += 1
			input_file.seek((file_number)*16*3)
			new_file.write(content)
		#break
'''
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
				if int(line[0:-1]) < 21 and count == 9:
					directory = 1
					file_name = file_name[0:-1]
				else:	
					file_name = file_name + line[0:-1].decode('hex')	
			if directory:				
				if count == 13:
					print file_name
					count = 0
					os.mkdir(file_name)
					directory = 0
					file_number = file_number + 1
					if(file_number == number_of_files):
						break
			else:			
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
					input_file.seek((cluster + 1)*13*3 + 3)
					new_file.write(content)
					file_number = file_number + 1
					if(file_number == number_of_files):
						break
'''
if __name__ == "__main__":
   main(sys.argv[1:])
