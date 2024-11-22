import pandas as pd
from pathlib import Path

from abner.Classes.Class_LogDataSet import LogDataSet
from abner.Classes.Class_FileName import FileName
from abner.Utilities.Functions_Units import (
    Get_Units_Recognized,
    Get_Depth_Variable_Unit,
)
from abner.Utilities.Say_It import Say_It


def CSV_to_LogDataSet_1W(PRJ, path_file, pars_input):

    print(f"{Path(__file__).stem} processing well: {path_file.stem}")
    set_units_recognized = Get_Units_Recognized(PRJ.dict_config["UnitsRecog"])
    LogDs = LogDataSet()

    # First read to check for units
    csv = pd.read_csv(path_file, nrows=1, na_values=["", " "])
    csv = csv.fillna("unitless").copy()

    # UNITS in the df?
    units_in = csv.iloc[0, :].tolist()

    set_units_in = set()
    [set_units_in.add(s.casefold()) for s in units_in]

    units_intersect = set_units_in.intersection(set_units_recognized)
    if len(units_intersect) == 0:
        Say_It("Well {LogsDs.wellName}  does NOT have  units, SET units, rerun again")
        return None
    else:
        csv = pd.read_csv(path_file, skiprows=range(1, 2))

    # WELLNAME
    if "wellName" in csv.columns:
        LogDs.wellName = str(csv.loc[csv.index[-1], "wellName"])
    else:
        LogDs.wellName = path_file.stem

    # SET rest
    LogDs.fileName = path_file.stem
    LogDs.format_in = "CSV"
    LogDs.nullValue = None
    LogDs.datasetName = "INPUTCSV"

    # Fill in df_varUnitInfo
    LogDs.df_varUnitInfo["var_in"] = csv.columns
    LogDs.df_varUnitInfo["unit_in"] = units_in
    LogDs.df_varUnitInfo["var_out"] = csv.columns
    LogDs.df_varUnitInfo["unit_out"] = [s.casefold() for s in units_in]
    LogDs.df_varUnitInfo["unitValid"] = None
    LogDs.df_varUnitInfo.index = csv.columns

    # Recognize  unitless as valid
    cond = LogDs.df_varUnitInfo["unit_in"] == "unitless"
    LogDs.df_varUnitInfo.loc[cond, "unitValid"] = True

    # SET DEPTH related variable/unit information
    dictUnit = dict(
        zip(LogDs.df_varUnitInfo.index, LogDs.df_varUnitInfo["unit_in"])
    )  # for historical reasons
    depth_variable, depth_unit = Get_Depth_Variable_Unit(PRJ.dict_config, dictUnit)
    LogDs.dict_depthInfo["depthName_in"] = depth_variable
    LogDs.dict_depthInfo["depthName"] = depth_variable
    LogDs.dict_depthInfo["depthUnit"] = depth_unit.casefold()

    LogDs.df = csv.copy()
    LogDs.pars_input = pars_input
    LogDs.moduleName = FileName(__file__).justName

    # Update history
    LogDs.UpdateHistory()

    # Save the LogDs object to a pickle file in the Input_Data & dir_prj folders
    if pars_input["save2pck"] == True:
        suf = "log.pck"
        the_suf = f"{path_file.stem}.{suf}"
        pckName_out = PRJ.dir_prj / "Input_Data" / the_suf
        LogDs.Save2Pck(pckName_out)

        pckName_in = PRJ.dir_prj / the_suf
        LogDs.Save2Pck(pckName_in)

    return LogDs
