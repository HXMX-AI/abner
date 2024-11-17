
from    pathlib                             import      Path
import  pickle
from    Utilities.Functions_Pickle_Files    import      Read_Pickle_File




#=======================================================================================================================
def Update_Project_WellInfo_1W(PRJ, *args):

    dir_prj   = PRJ.dir_prj
    PRJ_fName = dir_prj / 'PRJ.pck'
    with open(PRJ_fName, "rb") as input_file:
        PRJ = pickle.load(input_file)

    numWells, _      = PRJ.df_wellInfo.shape
    df_wellInfo      = PRJ.df_wellInfo.copy()

    # Add new fields to df_wellInfo
    df_wellInfo['nullDepth'] = 0
    df_wellInfo['Top']       = None
    df_wellInfo['Bottom']    = None


    numRows, numCols = df_wellInfo.shape

    df_wellInfo.index = range(numRows)

    # LOOP over each well
    for i in range(numRows):

        p_path = dir_prj / df_wellInfo.loc[i, 'path_pck']
        dso = Read_Pickle_File(p_path)


        # UPDATE depthUnit
        df_wellInfo.loc[i,'sampRate']    = dso.dict_depthInfo['sampRate']
        df_wellInfo.loc[i,'orgSampRate'] = dso.dict_depthInfo['orgSampRate']
        df_wellInfo.loc[i,'depthUnit']   = dso.dict_depthInfo['depthUnit']

        dict_depthInfo                 = dso.dict_depthInfo
        df_wellInfo.loc[i,'nullDepth'] = dict_depthInfo['numNulls']

        iTop                           = dso.df['DEPTH'].index[0]
        iBot                           = dso.df['DEPTH'].index[-1]
        df_wellInfo.loc[i, 'Top']      = dso.df.loc[iTop, 'DEPTH']
        df_wellInfo.loc[i,'Bottom']    = dso.df.loc[iBot, 'DEPTH']

    PRJ.df_wellInfo = df_wellInfo.copy()

    if True:
        outName = dir_prj / "PRJ_WellInfo.xlsx"
        PRJ.df_wellInfo.to_excel(outName, index = False)





    return PRJ, None



#
if __name__ == '__main__':

    project_name = "Junk_Nov14_test"     #     "ND_152N_101W_20241004_LAS_test"  # "LINSEG_TEST_2"
    dir_WELLS    = Path("C:/Users/ridva/OneDrive/Documents/WELLS")
    dir_prj      = dir_WELLS / project_name

    zart         = Update_Project_WellInfo_1W(dir_prj)

    print('done')