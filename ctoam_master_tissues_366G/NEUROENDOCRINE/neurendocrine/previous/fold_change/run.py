'''20200320 process today's data in paralell'''
import os
import multiprocessing as mp
def parfor(my_function, my_inputs, n_thread=mp.cpu_count()): # eval fxn in parallel, collect
    if n_thread == 1:
        result = []
        for i in range(len(my_inputs)):
            result.append(my_function(my_inputs[i]))
        return result
    else:
        pool = mp.Pool(n_thread)
        result = pool.map(my_function, my_inputs)
        return(result)

jobs = []

def run(c):
    jobs.append(' '.join(c) if type(c) == list else c)
pc = 'python3 fold_change.py'

# list jobs here
run([pc, 'INPUT/Armando_Baldassara_Exosomal_RNA.xlsx', 'REF/Breast_Normal_Tissue_new.xls'])
run([pc, 'INPUT/Armando_Baldassara_Exosomal_RNA.xlsx', 'REF/Gallbladder_Normal_Tissue.xls'])
run([pc, 'INPUT/Armando_Baldassara_Exosomal_RNA.xlsx', 'REF/Uterus_Normal_Tissue_27Mar22.xls'])


def ev(c):
    print(c)
    return os.system(c)

# evaluate
if __name__ == '__main__': 
    results = parfor(ev, jobs)
    print('done', results)
