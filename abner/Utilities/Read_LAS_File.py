# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:20:59 2024

@author: ridva
"""
import lasio
from    GUIs.GUI_GetFileName        import GUI_GetFileName
from    pathlib     import Path
#=================================
def Read_LAS_File(wd, fName):


    las         = lasio.read(wd+fName)
    df          = las.df()

    return las.well, df

#=============================================================
if __name__ == "__main__":
    # wd       = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
    # fName    = "15-9-19_SR_COMP.LAS"

    las_fileName = GUI_GetFileName('las')
    las_path     = Path(las_fileName)
    wd           = las_path.parent
    fName        = las_path.name


    header, df = Read_LAS_File(wd, fName)

    print('Done')