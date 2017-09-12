import numpy as np
import matplotlib.pyplot as plt
import re
import sys
import argparse
import logging

logging.basicConfig(format='%(asctime)s %(message)s',
                    stream=sys.stdout, level=logging.INFO)

parser = argparse.ArgumentParser(description='''transform the 2D NMR data into a Origin-friendly
                               format, where data is stored in a mixtrix with 
                               size ofn_row*n_col''')
parser.add_argument('filename', help='2D NMR data')
parser.add_argument('-n', '--normalize', action='store_true', help='normalize the data')
parser.add_argument('-p', '--plot', action='store_true', help='plot the figure')
parser.add_argument('-r', '--reverseF1', action='store_true', help='reverse F1 dimension')
args = parser.parse_args()

file = args.filename


def read_paramts(file):
    para = {'n_row': None, 'n_col': None, 'f1_left': None,
            'f1_right': None, 'f2_left': None, 'f2_right': None}
    num_lns = 0
    with open(file, 'r') as f:
        for line in f:
            num_lns += 1
            if not para['n_row']:  # re.findall('NROWS = (\d+)',line):
                para['n_row'] = re.findall('NROWS = (\d+)', line)
            if not para['n_col']:
                para['n_col'] = re.findall('NCOLS = (\d+)', line)
            if not para['f1_left']:  # re.findall('F1LEFT = ([+-]?([0-9]*[.])?[0-9]+) ppm.',line)
                para['f1_left'] = re.findall('F1LEFT = ([-]?[0-9]+[.][0-9]+) ppm.', line)
            if not para['f1_right']:
                para['f1_right'] = re.findall('F1RIGHT = ([-]?[0-9]+[.][0-9]+) ppm.', line)
            if not para['f2_left']:
                para['f2_left'] = re.findall('F2LEFT = ([-]?[0-9]+[.][0-9]+) ppm.', line)
            if not para['f2_right']:
                para['f2_right'] = re.findall('F2RIGHT = ([-]?[0-9]+[.][0-9]+) ppm.', line)
            if 'row = 0' in line:
                break
    for key, value in para.items():
        print(key, ':', value[0])
    print('no. of lines before data:', num_lns)
    if not para['n_row']:
        print('the input file is wrong')
    para['num_lns']=num_lns
    return para


def plt_fig(para, arr):
    arr_normalized = arr / np.amax(arr)
    x_start = float(para['f2_left'][0])
    x_end = float(para['f2_right'][0])
    x = np.linspace(x_start, x_end, num=int(para['n_col'][0]))
    y_start = float(para['f1_left'][0])
    y_end = float(para['f1_right'][0])
    if args.reverseF1:
        y = np.linspace(y_end, y_start, num=int(para['n_row'][0]))
    else:
        y = np.linspace(y_start, y_end, num=int(para['n_row'][0]))
    levels = [0.05, 0.07, 0.09, 0.12, 0.16, 0.22, 0.29, 0.39, 0.52, 0.70, 0.93]
    plt.figure()
    CS = plt.contourf(x, y, arr_normalized, levels, cmap=plt.cm.Spectral)
    plt.colorbar(CS)
    plt.xlim(x_start, x_end)  # plt.ylim(-.5, 1.5)#plt.clabel(CS, inline=1, fontsize=10)
    plt.title('2D plot')
    plt.show()


def main():
    para=read_paramts(file)
    arr = np.zeros((int(para['n_row'][0]), int(para['n_col'][0])))
    with open(file, 'r') as f:
        for i in range(int(para['num_lns'])):
            next(f)
        for i in range(int(para['n_row'][0])):
            for j in range(int(para['n_col'][0])):
                arr[i][j] = f.readline()
            f.readline()
    if args.normalize:
        arr_normalized = arr / np.amax(arr)
        np.savetxt('%s_normalized.dat' % file, arr_normalized, fmt='%.5f')
    else:
        np.savetxt('%s.dat' % file, arr, fmt='%.2f')

    if args.plot:
        plt_fig(para, arr)


if __name__ == "__main__":
    main()