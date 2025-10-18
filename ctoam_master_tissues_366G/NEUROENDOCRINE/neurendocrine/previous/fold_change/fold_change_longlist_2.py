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
         'RB1', 'RET', 'RICTOR', 'ROS1', 'RRM1', 'SLC34A2', 'TACSTD2', 
	 'TOP2A', 'TOP1', 'TP53',
         'TYMS', 'TSC1', 'TSC2', 'KDR', 'VHL', 'XPO1', 'TIAM1', 'TAL1', 
	 'TAL2', 'SET', 'HOXC10', 
	 'TRPM4', 'PRR11', 'CENPF', 'FOXM1', 'RHBDD2', 'HRAS', 'TERT', 
	 'LMO1', 'REL', 'NRG1', 'NRG2', 'NRG3', 'RARA', 'LMO2', 'MYCL1',  	 
	'RAF1', 'CCND1', 'PIM1', 'PBX1', 'TCF3', 'MIR7-3HG', 'MCF2L', 'MYCN', 
	'MOS', 'MLLT11', 'MDM2', 'LYL1', 'LCK', 'AKAP13', 'JUN', 'IL3RA', 
	'TLX1', 'GNAS', 'GLI1', 'FOS', 'CSF1R', 'EWSR1', 'FLI1', 'ETS1', 'ERG', 
	'DEK', 'MCF2', 'BCL2', 'BCL2L1', 'BCL3', 'BCL6', 'AXL', 'RUNX1', 'AFF4', 'TIAM1', 'TAL1', 'TAL2', 'SET', 'HOXC10', 'TRPM4', 'PRR11', 'CENPF', 'FOXM1', 'RHBDD2', 'HRAS', 'TERT', 'LMO1', 'LMO2', 'REL', 	'NRG1', 'NRG2', 'NRG3', 'RARA', 'RAF1', 'CCND1', 'PIM1', 'PBX1', 'TCF3', 'MIR7-3HG', 'MCF2L', 'MYCN', 'MOS', 'MLLT11', 'MDM2', 'LYL1', 'LCK', 'AKAP13', 'JUN', 'IL3RA', 'TLX1', 'GNAS', 'GLI1', 'FOS', 	'CSF1R', 'EWSR1', 'FLI1', 'ETS1', 'ERG', 'DEK', 'MCF2', 'BCL2', 'BCL2L1', 'AXL', 'RUNX1', 'AFF4', 'UHRF1', 'SOX2', 'FZD1', 'FZD2', 'FZD3', 'FZD4', 'FZD5', 'FZD7', 'FZD8', 'FZD10', 'STK40', 	'LRP5', 'LRP6', 	'LGR5', 'CELSR1', 'VANGL2', 'ROR1', 'ROR2', 'PTK7', 'SDC1', 'ORAI1', 'ORAI3', 'PIR', 'FABP7', 'MAEL', 'HES1', 'XIST', 'UCA1', 'LINC00115', 'LINC00339', 'SNHG3', 'SNHG12', 'DNM3OS', 	'LINC00467', 	'LINC00346', 'LINC00645', 'LINC00520', 'AURKAPS1', 'EMX2OS', 'KCNQ1OT1', 'MIR100HG', 'MIR17HG', 'MIR7-3HG', 'LINC00485', 'LOC338799', 'TPTE2P1', 'LINC00284', 'DLEU2', 'ATXN8OS', 'SNHG10', 	'MEG8', 	'DIO3OS', 'LINC00221', 'PWRN1', 'IPW', 'ULK4P2', 'LINC00673', 'LINC00511', 'SNHG16', 'LINC00470', 'LINC00668', 'UCA1', 'LINC00662', 'LINC00665', 'APOC1P1', 'KLKP1', 'MYCNOS', 'LOC389023', 	'LOC100131320', 	'PCGEM1', 'MGC16025', 'MIR155HG', 'LINC00515', 'LINC00161', 'LINC00310', 'LINC00160', 'LINC00114', 'DGCR9', 'TUG1', 'LINC00635', 'LINC00488', 'PCNAP1', 'SNHG8', 'LOC285419', 'PART1', 	'LINC00461', 'SNHG4', 	'LINC00518', 'HCG18', 'LINC00336', 'TDRG1', 'LOC730101', 'SNHG5', 'NHEG1', 'RAET1K', 'LINC00473', 'LOC441204', 'HOXA-AS3', 'LINC00265', 'SNHG15', 'LINC00525', 'LOC100129148', 	'FLJ40852', 'LOC389641', 	'SNHG6', 'LPCAT1', 'LOC100133669', 'RMRP', 'FAM201A', 'PCA3', 'LINC00092', 'SNHG7', 'XIST', 'FTX', 'LINC00630', 'BCAR4', 'CRNDE', 'LINC00304', 'LINC00324', 'LINC00514', 'FLJ22447', 	'LINC00239', 	'LINC00313', 'LINC00319', 'HOTTIP', 'PVT1', 'LINC00152', 'HOTAIR', 'H19', 'WRAP53', 'HOXD-AS1', 'LINC00339', 'MIAT', 'SNHG1', 'LINC00340', 'DLEU1', 'LINC00174', 'NEAT1', 'DANCR', 'SNHG7', 'MALAT1', 	'SUMO1P3', 'LINC00518', 'ITGB2-AS1', 'PIWIL1', 'PIWIL2', 'PIWIL4', 'HOXA-AS3', 'RHPN1-AS1', 'MATN1-AS1', 'FOXD2-AS1', 'SBF2-AS1', 'A2M-AS1', 'PCED1B-AS1', 'MAPKAPK5-AS1', 'TPT1-AS1', 'GABPB1-AS1', 'ADPGK', 	'LOXL1-AS1', 'MAPT-AS1', 'HOXB-AS3', 'CACNA1G-AS1', 'BAIAP2-AS1', 'MAFG-AS1', 'DLGAP1-AS1', 'LBX2-AS1', 'HOXD-AS2', 'TTN-AS1', 'CBR3-AS1', 'ITGB2-AS1', 'ACVR2B-AS1', 'EHHADH-AS1', 'DLG1-AS1', 'THAP9-AS1', 	'LEF1-AS1', 'INHBA-AS1', 'FEZF1-AS1', 'ZFHX4-AS1', 'PITPNA-AS1']

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

