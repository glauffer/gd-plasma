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


def split_data(data, out):
	'''
	Save one file for each arch's run
	'''
	delta = dist_module(data)
	desvio = np.std(delta)
	residuo = delta - desvio
	ciclo = np.zeros((data.T[1].size,2))
	k = 0
	j = 0
	indices = [] 
	for i in range(len(data.T[1])):
		try:
			if residuo[i] < desvio:
				ciclo[i] = data[i]
			elif residuo[i] >= desvio:
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


def dist_module(data):
	'''
	Calculates the distance modulus between two points
	'''
	pos_y = data.T[1] #utiliza apenas os dados em Y (posicao)
	delta = np.zeros(pos_y.size-1)
	for i in range(delta.size):
		delta[i] = abs(pos_y[i+1]-pos_y[i])
	return delta


def main():
	args = get_args()

	files = get_files(args.i)
	out = out_dir(args.o)


	for plasma in files:
		data = np.array(np.loadtxt(plasma))
		#size = min_peak(data, args.mean, args.std)
		split = split_data(data, out)


if __name__ == "__main__":
    exit(main())