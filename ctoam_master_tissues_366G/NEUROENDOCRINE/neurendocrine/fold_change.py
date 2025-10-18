''' fold_change.py 20220921 version. Usage:
python3 fold_change.py [patient RPM sample sheet] [reference RPM sample sheet folder]
'''
import os
import sys
import time
import math
import pandas as pd
from os import listdir
from codes import codes
from style import color_red, color_green, highlight_cells
from os.path import isfile, join, exists, isdir
args = sys.argv

def err(m):
    print('Error:', m); sys.exit(1)

def get(file_name): # pull a sheet out of excel file
    xl = pd.ExcelFile(file_name)
    sheet_name = xl.sheet_names[0] # take first sheet only
    return [sheet_name, xl.parse(sheet_name)]

def get_col(df, col_name):  # get a named col out of the sheet
    return list(df.loc[:, col_name])

if len(args) < 3:
    err('fold_change.py # Usage (in Terminal.app):\n  ' +
        'python3 fold_change.py [patient sample RPM sheet] [folder of reference RPM sheets]')

data_file = args[1]  # patient sample RPM sheet
norm_folder = args[2]  # folder w multiple tissue sample reference files

isnan, NaN = math.isnan, math.nan  # initial values

if not exists(data_file) and isfile(data_file):  # check inputs exist
    err('please check data file:', data_file)
if not exists(norm_folder) and isdir(norm_folder):
    err('please check reference data folder:', norm_folder)

[data_sheet_name, data] = get(data_file) # load patient file
contig_id =  get_col(data, 'contig_id') # patient sample contig_id
RPM = get_col(data, 'RPM') # patient sample RPM 

# =============================================================================
# 20220221 modification to add a second, shortened sheet
attr = get_col(data, 'attributes')
lookup2 = {}
for i in range(len(attr)):
    lookup2[attr[i].split(';')[0].split('=')[1]] = i

# for c in codes: print(c, lookup2[c])
ix_c = [lookup2[c] for c in codes]
data3 = pd.DataFrame()  # data frame to store shortened sheet before writing
#==============================================================================

# look for reference sheets
files = [join(args[2], f)  # path to file
         for f in listdir(norm_folder)  # for everything in the folder
         if isfile(join(norm_folder, f))]  # that is a file!

norm_file_index = -1
normal_cols, normal_cols_2 = [], []
fold_change_cols, fold_change_cols_2 = [], []
for norm_file in files:
    norm_file_index += 1  # track which reference file we're on
    print('  +r', norm_file) # , norm_file_index)
    fn = norm_file.split(os.path.sep)[-1]
    # print("FN", fn)
    space_start = fn.split(' ')[0]
    under_start = fn.split('_')[0]
    tissue_type = space_start if len(space_start) < len(under_start) else under_start

    [data_sheet_name2, data2] = get(norm_file) # load reference file
    contig_id2 = get_col(data2, 'contig_id') # contig_id for normal reference values
    RPM2 = get_col(data2, 'RPM') # NB match on contig id before copying over

    N = len(contig_id)
    RPM_normal, contig_id_normal = [NaN for i in range(N)],\
                                   [NaN for i in range(N)]
    fold_change = [NaN for i in range(N)] # fold change

    # calculate the row index for the record containing a given contig-id
    lookup = {contig_id2[i]: i for i in range(len(contig_id2))}

    for i in range(N):
        ix = contig_id[i] # contig id this patient sample
        RPM_normal[i] = RPM2[lookup[ix]] # get ref expression level, same contig_id
        contig_id_normal[i] = contig_id2[lookup[ix]]  # confirm contig_id matches!
        # reference is "old", patient sample is new...
        # 1) increase: new / original 2) decrease: original / new..
        new, old = RPM[i], RPM_normal[i]
        try:
            fold_change[i] = (new / old) if (new >= old) else\
                             -1. * (old / new)
        except:
            pass

        # replace fold change value with patient RPM value if reference RPM not measured
        try:
            fold_change[i] = fold_change[i] if old > 0 else ("*" + str(new))
            if (old <=0 and new <=0):  # don't record fold change if both values are zero
                fold_change[i] = NaN
        except:
            pass

    # add cols to write to new spreadsheet
    data['normal_RPM_' + tissue_type] = RPM_normal
    data['normal_contig_id_' + tissue_type] = contig_id_normal
    data['fold_change_' + tissue_type] = fold_change
    fold_change_cols += ['fold_change_' + tissue_type]
    normal_cols += ['normal_RPM_' + tissue_type]


    # add cols to write to short spreadsheet
    if norm_file_index == 0:  # only add patient RPM value once (at beginning) to avoid repeating same data
        data3['RPM'] = [RPM[i] for i in ix_c]  # i.e. not for every reference tissue sheet
        data3['Gene_Symbol'] = codes

    data3['RPM_normal_' + tissue_type] = [RPM_normal[i] for i in ix_c]
    data3['Fold_Change_' + tissue_type] = [fold_change[i] for i in ix_c]
    fold_change_cols_2 += ['Fold_Change_' + tissue_type]
    normal_cols_2 += ['RPM_normal_' + tissue_type]

# color the new sheet
# data.style.applymap(color_red, subset=['RPM'])

# write the new sheet
ofn = data_file.replace(' ', '_').replace('.xlsx', '').replace('.xls', '') + '_output.xlsx'
if ofn[:6] == 'INPUT/':
    ofn = ofn.replace('INPUT/', 'OUTPUT/')
print('  +w', ofn)
try:
    data.style.applymap(color_red, subset=['RPM'])\
              .applymap(color_green, subset=normal_cols)\
              .applymap(highlight_cells, subset=fold_change_cols)\
              .to_excel(ofn,
                        sheet_name=data_sheet_name,
                        index=True,
                        engine='openpyxl')
except:
    data.to_excel(ofn, sheet_name=data_sheet_name, index=True, engine='openpyxl')
# data.to_excel(ofn, sheet_name = data_sheet_name, index=True)

# write the shortened sheet
ofn2 = data_file.replace(' ', '_').replace('.xlsx', '').replace('.xls', '') + '_output_SHORT.xlsx'
if ofn2[:6] == 'INPUT/':
    ofn2 = ofn2.replace('INPUT/', 'OUTPUT/')
print('  +w', ofn2)
try:
    data3.style.applymap(color_red, subset=['RPM'])\
               .applymap(color_green, subset=normal_cols_2)\
               .applymap(highlight_cells, subset=fold_change_cols_2)\
               .to_excel(ofn2,
                         sheet_name=data_sheet_name,
                         index=False,
                         engine='openpyxl')
except:
    data3.to_excel(ofn2, sheet_name=data_sheet_name, index=False, engine='openpyxl')
# data3.to_excel(ofn2, sheet_name = data_sheet_name, index=False)
