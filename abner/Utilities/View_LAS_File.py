# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:20:59 2024

@author: ridva
"""
import lasio
from    GUIs.GUI_GetFileName        import GUI_GetFileName
from    pathlib     import Path




#=================================
def View_LAS_File(las_path, numLines= 10):


    las         = lasio.read(las_path)
    df          = las.df()

    print(f'\n {las.curves}')
    print(f'\nInput file full path: {str(las_path)}')
    print('\n', df.head(numLines) )
    print( df.tail(numLines) )

    return las.well, df





#=============================================================
if __name__ == "__main__":
    # wd       = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
    # fName    = "15-9-19_SR_COMP.LAS"

    las_fileName = GUI_GetFileName('las')
    las_path     = Path(las_fileName)
    _            = View_LAS_File(las_path)

    print('Done')