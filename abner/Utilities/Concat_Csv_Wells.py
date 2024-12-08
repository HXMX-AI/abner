"""
    Code used to comcatenate files for the CoreGeologic Project
    Beni dinlemeyenleri oldurmem gerek, oglum, tek kuyu, tek file.
    Isin yoksa ugras, al sana, gece yarisi
    Nov 14, 2024
"""




import pandas as pd
from pathlib import Path

if False:
    wd     = "C:/Users/ridva/OneDrive/Documents/WELLS/CoreGL_REDO/TO_JAMES"
    fName1 = "33053031400000-AIG.csv"
    fName2 = "33053031400000-AIG-CND.csv"


    file1 = Path(wd) / fName1
    file2 = Path(wd) / fName2

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    #Variables
    df1.shape
    df2.shape

    set1 = set(df1.columns)
    set2 = set(df2.columns)

    set_diff = set1-set2 if len(set1) > len(set2) else set2-set1
    print(set_diff)

    #


    df_out = pd.DataFrame(columns = df2.columns)
    df_out = pd.concat([df1.iloc[:11121,:], df2.iloc[1:,:]], ignore_index=True)

    fNameOut = wd + '/' + fName1[:-4] + '_merged.csv'
    df_out.to_csv(fNameOut, index=False)



wd     = "C:/Users/ridva/OneDrive/Documents/WELLS/CoreGL_REDO/TO_JAMES"
fName1 = "33053030990000-AIG-CAL.csv"
fName2 = "33053030990000-AIG-CND.csv"


file1 = Path(wd) / fName1
file2 = Path(wd) / fName2

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

#Variables
df1.shape
df2.shape

set1 = set(df1.columns)
set2 = set(df2.columns)

set_diff = set1-set2 if len(set1) > len(set2) else set2-set1
print(set_diff)

#


df_out = pd.DataFrame(columns = df2.columns)
df_out = pd.concat([df1, df2.iloc[1:,:]], ignore_index=True)

fNameOut = wd + '/' + fName1[:-4] + '_merged.csv'
df_out.to_csv(fNameOut, index=False)