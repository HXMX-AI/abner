"""
    This module replaces incoming variable names with those defined in the
    harmonization table, df_harm.
    var_out in df_varUnitInfo is set to the first match for a given harm variable
    If an alias is not found, the incoming variable name is kept.
    dictUnit_in has the incoming variable names and units.
    dictUnit    has the standard variable names and incoming units.
"""

import pandas as pd
from pathlib import Path
import numpy as np


def Harmonize_Variables_1W(PRJ, p_path, pars_input, dso):

    # STANDARD BOOKEEPING .......................................
    dso.moduleName = Path(__file__).stem
    dso.pars_input = pars_input.copy()
    if pars_input["saveDebug"]:
        dso.Save2Pck_Debug(str(p_path))

    print(f"{Path(__file__).stem} processing well: {p_path.stem}")

    # Prepare df_config to be used in alias matching .............................
    temp1 = PRJ.dict_config["Harmonization"].drop(
        ["Unit", "Min", "Max", "Type"], axis=1
    )
    temp2 = pd.Series(temp1.index.tolist(), index=temp1.index)
    df_harm = pd.concat(
        [temp2, temp1], axis=1, ignore_index=True
    )  # Original name comes first
    df_harm_bool = pd.DataFrame(
        np.zeros(df_harm.shape), dtype=bool, index=df_harm.index
    )
    del temp1, temp2

    # Which varNames are in df_harm?
    for varSearch in dso.df_varUnitInfo.index:
        cond = df_harm == varSearch
        df_harm_bool += cond

    # Set var_out to the first match for a given varHarm, leave others alone
    for varHarm in df_harm.index:
        list_varHarm = list(df_harm.loc[varHarm, :][df_harm_bool.loc[varHarm, :]])
        if len(list_varHarm):
            dso.df_varUnitInfo.loc[list_varHarm[0], "var_out"] = varHarm

    # Update columns in dso.df, update df_varInfo index now that variable names are updated
    dictColumnsNew = dict(
        zip(dso.df_varUnitInfo["var_in"], dso.df_varUnitInfo["var_out"])
    )
    dso.df.rename(columns=dictColumnsNew, inplace=True)

    # Update df_varUnitInfo index, and dict_depthInfo
    dso.df_varUnitInfo.index = dso.df_varUnitInfo["var_out"]
    dso.dict_depthInfo["depthName"] = (
        "DEPTH"  # by default, after harmomization, reference variable is DEPTH
    )

    # HISTORY
    dso.UpdateHistory()

    # SAVE
    if pars_input["save2pck"]:
        dso.Save2Pck(p_path)

    return PRJ, dso
