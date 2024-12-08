from pathlib import Path
from abner.Utilities.Functions_Pickle_Files import Read_Pickle_File
import numpy as np
from abner.Classes.Class_ImmutableDataFrame import ImmutableDataFrame


# =======================================================================================================================
def WellInfo_Update_1W(PRJ, p_path, pars_input, dso):

    #
    idx = dso.p_path.name
    PRJ.df_wellInfo.loc[idx, "wellName"] = dso.wellName
    PRJ.df_wellInfo.loc[idx, "orgAPI"] = dso.orgAPI
    PRJ.df_wellInfo.loc[idx, "API"] = dso.API
    PRJ.df_wellInfo.loc[idx, "UWI"] = dso.UWI
    PRJ.df_wellInfo.loc[idx, "orgSampRate"] = dso.dict_depthInfo["orgSampRate"]
    PRJ.df_wellInfo.loc[idx, "sampRate"] = dso.dict_depthInfo["sampRate"]
    PRJ.df_wellInfo.loc[idx, "depthUnit"] = dso.dict_depthInfo["depthUnit"]
    PRJ.df_wellInfo.loc[idx, "duplVars"] = dso.duplVars
    PRJ.df_wellInfo.loc[idx, "keep"] = 1
    PRJ.df_wellInfo.loc[idx, "path_pck"] = p_path

    PRJ.df_wellInfo.loc[idx, "nullDepth"] = dso.dict_depthInfo["numNulls"]
    PRJ.df_wellInfo.loc[idx, "Top"] = dso.df.loc[0, "DEPTH"]
    PRJ.df_wellInfo.loc[idx, "Bottom"] = dso.df.loc[dso.df.index[-1], "DEPTH"]

    return PRJ, None
