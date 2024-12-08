from pathlib import Path
import pickle
from abner.Utilities.Functions_Pickle_Files import Read_Pickle_File


# =======================================================================================================================
def Project_Summary_Standard_Create(PRJ, *args):

    PRJ_fName = dir_prj / "PRJ.pck"
    with open(PRJ_fName, "rb") as input_file:
        PRJ = pickle.load(input_file)

    numWells, _ = PRJ.df_wellInfo.shape
    df_wellInfo = PRJ.df_wellInfo.copy()
    numRows, numCols = df_wellInfo.shape

    # LOOP over each well
    for i in df_wellInfo.index:

        p_path = dir_prj / df_wellInfo.loc[i, "path_pck"]
        dso = Read_Pickle_File(p_path)

        # UPDATE depthUnit
        df_wellInfo.loc[i, "sampRate"] = dso.dict_depthInfo["sampRate"]
        df_wellInfo.loc[i, "orgSampRate"] = dso.dict_depthInfo["orgSampRate"]
        df_wellInfo.loc[i, "depthUnit"] = dso.dict_depthInfo["depthUnit"]

        dict_depthInfo = dso.dict_depthInfo
        df_wellInfo.loc[i, "nullDepth"] = dict_depthInfo["numNulls"]

        iTop = dso.df["DEPTH"].index[0]
        iBot = dso.df["DEPTH"].index[-1]
        df_wellInfo.loc[i, "Top"] = dso.df.loc[iTop, "DEPTH"]
        df_wellInfo.loc[i, "Bottom"] = dso.df.loc[iBot, "DEPTH"]

    PRJ.df_wellInfo = df_wellInfo.copy()
    print(f"\n{df_wellInfo}")

    if True:
        outName = dir_prj / "Project_Summary_Standard.xlsx"
        PRJ.df_wellInfo.to_excel(outName, index=True)
    return PRJ, None


#
if __name__ == "__main__":

    project_name = "Sunday_test"  #   "WB_20241118_CoreGeo"     #  "CoreGL_REDO"     #     "ND_152N_101W_20241004_LAS_test"  # "LINSEG_TEST_2"
    dir_WELLS = Path("C:/Users/ridva/OneDrive/Documents/WELLS")
    dir_prj = dir_WELLS / project_name

    zart = Project_Summary_Standard_Create(dir_prj)

    print("done")
