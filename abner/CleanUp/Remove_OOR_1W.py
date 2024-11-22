import pandas as pd
import pickle

from abner.Classes.Class_FileName import FileName
from abner.Utilities.FilesInDir import FilesInDir
from abner.Utilities.Functions_Misc import Check_All_Bool


def Remove_OOR_1W(PRJ, p_path, pars_input, dso):

    dso.moduleName = FileName(__file__).justName
    dso.pars_input = pars_input.copy()
    if pars_input["saveDebug"]:
        dso.Save2Pck_Debug(str(p_path))

    df_harm = PRJ.dict_config["Harmonization"]
    remove_OORs = PRJ.dict_config["Misc"].loc["remove_OORs"].iloc[0]
    save_df_OOR = PRJ.dict_config["Misc"].loc["save_df_OOR"].iloc[0]

    theCols = set(dso.df_varUnitInfo["var_out"]).intersection(set(df_harm.index))
    theShape = dso.df.shape
    theShape = (theShape[0], len(theCols))

    df_flag = pd.DataFrame(None, columns=list(theCols), index=list(dso.df.index))
    for var in theCols:
        if var in df_harm.index:
            x_left = df_harm.loc[var, "Min"]
            x_right = df_harm.loc[var, "Max"]
            cond = dso.df[var].between(
                x_left, x_right, inclusive="both"
            )  # Negate, want to know bad
            df_flag.loc[:, var] = cond.copy()

    # IMPORTANT
    # number_none + number_in_range + number_out_range = number_of_variables in oor
    df_flag_sum = df_flag.sum(axis=1)
    df_none = dso.df[list(theCols)].isna()
    df_none_sum = df_none.sum(axis=1)
    N = len(df_none.columns)
    num_oor_per_row = N - (df_flag_sum + df_none_sum)

    df_flag = df_flag.astype(bool)  # needed for using the flag as an index
    df_flag = ~df_flag.copy()
    if remove_OORs == True:
        dso.df[df_flag] = None

    # FL_OOR, set
    FL_OOR = pd.Series(0, index=list(dso.df.index))
    cond = num_oor_per_row >= 1
    FL_OOR[cond] = 1

    # Update df and variable lists
    dso.df["FL_OOR"] = FL_OOR
    dso.Add_Variable(FL_OOR.astype(int), "FL_OOR", "unitless")

    # ADD flag, save df_OOR for debugging if asked for
    if save_df_OOR == True:
        df_flag["FL_ALL"] = FL_OOR.copy()
        dso.df_OOR = df_flag.copy()

    # HISTORY
    dso.UpdateHistory()
    # SAVE to pck
    if pars_input["save2pck"]:
        dso.Save2Pck(p_path)

    # MESSAGE
    if remove_OORs:
        print(f"Removed OORs  well: {p_path}")
    else:
        print(f"Ran Remove_OOR_1W on {p_path}")

    return PRJ, dso


if __name__ == "__main__":

    # CONFIG stuff
    dir_config = "C:/Users/ridva/OneDrive/Documents/WELLS/"
    fName_config = "config_logRcnd.xlsx"
    df_null = pd.read_excel(dir_config + fName_config, sheet_name="Nulls")

    # INPUT pck files
    dir_prj = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
    fileNames = FilesInDir(dir_prj)

    if not fileNames:
        raise ValueError("No pck files found")

    for pckFileName in fileNames:
        with open(pckFileName, "rb") as file:
            dso = pickle.load(file)

        # pars_input
        pars_input = {}
        pars_input["pckFileName"] = pckFileName
        pars_input["nullList"] = df_null
        pars_input["save2pck"] = True
        pars_input["saveDebug"] = False
        # Add PRJ and p_path parameters
        PRJ = None  # Initialize PRJ as needed
        p_path = pckFileName  # Using the pickle file path
        new_dso = Remove_OOR_1W(PRJ, p_path, pars_input, dso)

    print("done")
