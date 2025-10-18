''' python3 fold_change.py. based on 20220214_combine_sheets.py

This script combines a patient RPM sample sheet with a normal tissue sample RPM sheet
and adds fold change column.  e.g. use at terminal:

python3 fold_change.py Joshua_Yoneda_Jan_17_2022_output.xlsx Spinal_Cord_Normal_Feb_10_2022.xls

20220221 modified to add a second, shortened sheet'''
import pandas as pd
import os, sys, time, math
args = sys.argv
data_file = args[1] # patient file
norm_file = args[2] # normal tissue sample reference file to combine 
isnan, NaN = math.isnan, math.nan

def get(file_name): # pull a sheet out of excel file
    xl = pd.ExcelFile(file_name)
    sheet_name = xl.sheet_names[0] # take first sheet only
    return [sheet_name, xl.parse(sheet_name)]

def get_col(df, col_name):  # get a named col out of the sheet
    return list(df.loc[:, col_name])

[data_sheet_name, data] = get(data_file) # load patient file
[data_sheet_name2, data2] = get(norm_file) # load reference file

contig_id =  get_col(data, 'contig_id') # patient sample contig_id
RPM = get_col(data, 'RPM') # patient sample RPM 

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
    except: pass 
# add cols to write to new spreadsheet
data['normal_RPM'] = RPM_normal
data['normal_contig_id'] = contig_id_normal
data['fold_change'] = fold_change

# write the new sheet
ofn = data_file.replace(' ', '_').replace('.xlsx', '') + '_output.xlsx'
if ofn[:6] == 'INPUT/': ofn = ofn.replace('INPUT/', 'OUTPUT/')
print('+w', ofn)
data.to_excel(ofn, sheet_name = data_sheet_name, index=True)

# 20220221 modification to add a second, shortened sheet
attr = get_col(data, 'attributes')
lookup2 = {}
for i in range(len(attr)):
    lookup2[attr[i].split(';')[0].split('=')[1]] = i

codes = ['ADRB1', 'AKT1', 'AKT2', 'AKT3', 'ALK', 'APC', 'AR', 'ATM',
         'BAP1', 'BIRC5', 'BIRC7', 'BRAF', 'BRCA1', 'BRCA2', 'BTK',
         'CD3D', 'CD8A', 'CDK4', 'CDK6', 'CTLA4',
         'DDR2',
         'EGFR', 'ERBB2', 'ERBB3', 'ESR1', 'EZH2', 
         'FGFR1', 'FGFR2', 'FGFR3', 'FGFR4', 'FOLR1', 'F3',
         'EPAS1',
         'IDH1', 'IDH2',
         'MKI67', 'KIT', 'KRAS', 'LGALS3', 
         'MAP2K1', 'MET', 'MLH1', 'MMP9', 'MSH2', 'MSH3',
         'MSH6', 'MTOR',
         'NRAS', 'NTRK1', 'NTRK2', 'NTRK3',
         'PDCD1', 'CD274', 'PDCD1LG2', 'PDGFRA', 'PDGFRB',
         'PIK3CA', 'PVRL4', 'PMS1', 'PMS2', 'POLD1', 'POLE', 
         'PRR4', 'PTEN', 'SRC',
         'RB1', 'RET', 'RICTOR', 'ROS1', 'RRM1', 'SLC34A2', 'TACSTD2', 'TOP2A', 'TOP1', 'TP53',
         'TYMS', 'TSC1', 'TSC2', 'KDR', 'VHL', 'XPO1']

# for c in codes: print(c, lookup2[c])
ix = [lookup2[c] for c in codes]
data3 = pd.DataFrame()
data3['Gene Symbol'] = codes
data3['RPM'] = [RPM[i] for i in ix]
data3['RPM_normal'] = [RPM_normal[i] for i in ix]
data3['Fold Change'] = [fold_change[i] for i in ix]

ofn2 = data_file.replace(' ', '_').replace('.xlsx', '') + '_output_SHORT.xlsx'
if ofn2[:6] == 'INPUT/': ofn2 = ofn2.replace('INPUT/', 'OUTPUT/')
print('+w', ofn2)
data3.to_excel(ofn2, sheet_name = data_sheet_name, index=False)

