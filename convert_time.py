import numpy as np
import matplotlib.pyplot as plt


def rephase(data, period, col=0, copy=True):
    '''
    transform the time of observations to the phase space
    '''
    rephased = np.ma.array(data, copy=copy)
    rephased[:, col] = get_phase(rephased[:, col], period)
    return rephased


def get_phase(time, period):
    '''
    divide the time of observations by the period
    '''
    return (time / period) % 1


def convert_dt(data, new_dt, old_dt=33e-3):
    #convert = (new_dt / old_dt) * data.T[0]
    data[:, 0] = (new_dt / old_dt) * data.T[0]
    convert = data
    return convert

def main():
    data_path = '/home/glauffer/Dropbox/Research/Plasma/dados/tempo_posicao/1teste_b17a45_manual_completo.txt'
    data = np.array(np.loadtxt(data_path))
    p = 1 / 60
    correct_time = convert_dt(data, 1.33e-3)
    phased = rephase(correct_time, p)
    plt.plot(phased.T[0], np.abs(phased.T[1]), '-o')
    #plt.plot(correct_time.T[0], np.abs(correct_time.T[1]), '-o')
    plt.show()

if __name__ == "__main__":
    exit(main())
