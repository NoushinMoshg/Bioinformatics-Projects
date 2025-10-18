# fold_change utility
## Setup:
```
python3 -m pip install xlrd openpyxl pandas
```
## Instructions:
* Download **cleanup_filenames.py**, **fold_change.py**, **codes.py**, **style.py**, **run.py** and place them in your working folder
* Within your working folder, make sure you have created an **INPUT** folder, and a **REF** folder
* Inside the **INPUT** folder, create two more folders: **FEMALE** and **MALE**
* Inside the **REF** folder, create two more folders: **FEMALE** and **MALE**
* Patient sample RPM files for females go in the **INPUT/FEMALE** folder
* Patient sample RPM files for males go in the **INPUT/MALE** folder
* Reference RPM files for males go in the **REF/MALE** folder
* Reference RPM files for females go in the **REF/FEMALE** folder
* Correct the filenames by running: 
```
python3 cleanup_filename.py
```

To run the fold_change utility, in Terminal.app type:
```
python3 run.py
```
and press return.

* Outputs should appear in the two folders: **OUTPUTS/FEMALE** and **OUTPUTS/MALE** accordingly

## Test output:
Supposing that the test data contents were:
```
./REF/FEMALE/Falopian_4.27_mb.xls
./REF/FEMALE/Ovary_3.28_mb.xls
./INPUT/FEMALE/Kathy_Langlois_Transcriptome_March_3_2022.xls
```
the expected console output is:
```
MALE/:
FEMALE/:
  python3 fold_change.py INPUT/FEMALE/Kathy_Langlois_Transcriptome_March_3_2022.xls REF/FEMALE/
python3 fold_change.py INPUT/FEMALE/Kathy_Langlois_Transcriptome_March_3_2022.xls REF/FEMALE/
  +r REF/FEMALE/Falopian_4.27_mb.xls
  +r REF/FEMALE/Ovary_3.28_mb.xls
  +w OUTPUT/FEMALE/Kathy_Langlois_Transcriptome_March_3_2022_output.xlsx
  +w OUTPUT/FEMALE/Kathy_Langlois_Transcriptome_March_3_2022_output_SHORT.xlsx
done [0]
```
