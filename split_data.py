from argparse import ArgumentParser, FileType
import os
import numpy as np


def get_args():
    parser = ArgumentParser(description='Split the runs of each arch \
    						on a separeted file')
    
    parser.add_argument('-i', type=str, default=None,
    					help='Location or file of data')
    
    parser.add_argument('-o', type=str, default=None,
    					help='Location for output files')

    parser.add_argument('-mean', type=float, default=0.0,
    					help='factor to multiple the mean of the data')
    
    parser.add_argument('-std', type=float, default=2.0,
    					help='factor to multiple the std of the data')
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


def split_data(data, size, out):
	'''
	Save one file for each arch's run
	'''
	mag = data.T[1]
	ciclo = np.zeros((mag.size,2))
	k = 0
	j = 0
	for i in range(len(mag)):
		try:
			variacao = abs(mag[i+1]-mag[i])
			if variacao < size:
				ciclo[i] = data[i]
			elif variacao >= size:
				ciclo[i] = data[i]
				k = k+1
				np.savetxt(os.path.join(out,'ciclo_'+str(k)+'.txt'),
							ciclo[j:(i+1)], fmt = '%s')
				j = i + 1
		except IndexError:
			ciclo[i] = data[i]
			k = k + 1
			np.savetxt(os.path.join(out, 'ciclo_'+str(k)+'.txt'),
						ciclo[j:], fmt='%s')
	return None

def min_peak(data, meann, stdd):
	'''
	find the smallest peak
	'''
	mag = data.T[1]
	delta = np.zeros(mag.size-1)
	for i in range(delta.size):
		delta[i] = abs(mag[i+1]-mag[i])
    
	offset = meann*delta.mean() + stdd*delta.std()
	delta_max = np.zeros(delta.size)
	for i in range(delta.size):
		if delta[i] > offset:
			delta_max[i] = delta[i]
        
	masked_delta_max = np.ma.masked_equal(delta_max, 0.0, copy=False)
	return masked_delta_max.min()

def main():
	args = get_args()

	files = get_files(args.i)
	out = out_dir(args.o)


	for plasma in files:
		data = np.array(np.loadtxt(plasma))
		size = min_peak(data, args.mean, args.std)
		split = split_data(data, size, out)

if __name__ == "__main__":
    exit(main())