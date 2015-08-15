from argparse import ArgumentParser, FileType
import os
import numpy as np


def get_args():
    parser = ArgumentParser(description='Program to calculate the period \
    						of a star using the Conditional Entropy method')
    
    parser.add_argument('-i', type=str, default=None,
    					help='Location or file of stellar data')
    
    parser.add_argument('-o', type=str, default=None,
    					help='Location for output files')
    
    args = parser.parse_args()
    
    return args


def get_files(data):
	'''
	Get the correct path of file or files inside a directory
	'''
	if os.path.isfile(data):
		return [data]
		
	elif os.path.isdir(os.path.abspath(data)):
		path = os.path.abspath(data)
		os.chdir(path)
		list_of_files = os.listdir(path)
		return sorted(list_of_files)


def out_dir(out):
	'''
	check if the output path is relative or not and return the absolute path 
	'''
	if out == None:
		return os.getcwd()
	elif os.path.isdir(out):
		return os.path.abspath(out)


def main():
	args = get_args()

	files = get_files(args.i)
	out = out_dir(args.o)

	for plasma in files:
		data = np.array(np.loadtxt(plasma))


if __name__ == "__main__":
    exit(main())