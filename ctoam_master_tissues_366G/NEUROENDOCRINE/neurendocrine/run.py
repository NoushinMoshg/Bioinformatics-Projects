'''run.py  20220921 version. How to run:
    python3 fold_change.py 

Instructions:
    place patient RPM sample sheets in folder: 
        INPUT/MALE/ (for male patients)
        INPUT/FEMALE/ (for female patients)

    place reference RPM sample sheets in folder:
        REF/MALE/ (for male patients)
        REF/FEMALE/ (for female patients)

Note: outputs will appear in:
    OUTPUT/FEMALE/ and
    OUTPUT/MALE/ (respectively).
'''
import os
import sys
from os import listdir
import multiprocessing as mp
from os.path import isfile, exists, isdir, sep

def err(m):
    print('Error:', m); sys.exit(1)

def parfor(my_function, my_inputs, n_thread=mp.cpu_count()): # eval fxn in parallel, collect
    return [my_function(i) for i in my_inputs] if n_thread == 1 else mp.Pool(n_thread).map(my_function, my_inputs)

def check_folder(f, create=False):
    if type(f) == list:
        for i in f:
            check_folder(i, create)
    else:
        if not exists(f) or not isdir(f):
            if create:
                os.mkdir(f)
            else:
                err('please check required folder: ' + f)

check_folder(['INPUT' + sep + 'FEMALE',
              'INPUT' + sep + 'MALE',
              'REF' + sep + 'FEMALE',
              'REF' + sep + 'FEMALE'])

check_folder(['OUTPUT',
              'OUTPUT' + sep + 'FEMALE', 
              'OUTPUT' + sep + 'MALE'],
               create=True)

# list the input groups
groups = listdir(os.getcwd() + sep + 'INPUT' + sep)

# now, list the commands to be run:

jobs = []

for g in groups:
    print(g + sep + ':')
    patient_sheets = []
    x = listdir('INPUT' + sep + g)
    for i in x:
        if (i[-4:] == '.xls' or i[-5:] == '.xlsx'):
            patient_sheets += [i]
            # print('  ' + patient_sheets[-1])
            jobs.append(' '.join(['python3',
                                  'fold_change.py',
                                  'INPUT' + sep + g + sep + i,
                                  'REF' + sep + g + sep]))
            print('  ' + jobs[-1])

def run(c):
    print(c)
    return os.system(c)

# evaluate
if __name__ == '__main__': 
    results = parfor(run, jobs, 1)
    print('done', results)
