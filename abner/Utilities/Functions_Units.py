from pathlib import Path
from abner.Utilities.Say_It import Say_It


# =============================================================================
def Get_Dict_DepthInfo(varList, units_in, dict_config):

    set_units_recognized = Get_Units_Recognized(dict_config["UnitsRecog"])

    # UNITS in the df?
    set_units_in = set()
    [set_units_in.add(s.casefold()) for s in units_in]

    units_intersect = set_units_in.intersection(set_units_recognized)
    if len(units_intersect) == 0:
        Say_It("Well {LogsDs.wellName}  does NOT have  units, SET units, rerun again")
        return None

    # HAS UNITS, CONTINUE populating
    dictUnit = dict(zip(varList, units_in))
    dictUnit_in = dictUnit.copy()

    # SET DEPTH and its unit, if it exists
    depth_variable, depth_unit = Get_Depth_Variable_Unit(dict_config, dictUnit)
    depthName_in = depth_variable
    depthUnit = depth_unit

    return dictUnit, dictUnit_in, depthName_in, depthUnit


# ==================================================================================
def Get_Units_Recognized(df_unitsRecog):

    list_unitNames = sum(df_unitsRecog.iloc[:, 0:].astype(str).values.tolist(), [])
    tmp_unitNames = set(list_unitNames)
    if "nan" in tmp_unitNames:
        tmp_unitNames.remove("nan")

    set_units_recognized = set()
    [set_units_recognized.add(s.casefold()) for s in tmp_unitNames]

    return set_units_recognized


# ==================================================================================
def Get_Depth_Variable_Unit(dict_config, dictUnit):

    depth_variable_name = None
    depth_variable_unit = None

    df_Harmonization = dict_config["Harmonization"].copy()
    column_names = df_Harmonization.columns.tolist()
    temp = [s for s in column_names if "Unnamed" in s]
    depth_variables_recognized = df_Harmonization.loc["DEPTH", temp[0] :].tolist()
    depth_variables_recognized.append("DEPTH")

    df_variables = list(dictUnit.keys())
    set_depth_variables = set(df_variables).intersection(
        set(depth_variables_recognized)
    )

    # DEPTH name and unit
    if len(set_depth_variables) == 1:
        depth_variable_name = list(set_depth_variables)[0]
    depth_variable_unit = dictUnit[depth_variable_name]

    return depth_variable_name, depth_variable_unit


# =========================================================================================
def Get_Dict_Conv(df_unitConv, unit_in, unit_out):

    # Reformatting df_unitConv for easier search as it contains indices with the same value
    df_temp = df_unitConv.copy()
    dict_conv = {
        "unit_in": unit_in.lower(),
        "unit_out": unit_out.lower(),
        "bias": 0,
        "mult": 1,
    }

    # FIRST LINE of checks, is the unit conversion defined or is it necessary?
    if (unit_in not in list(df_temp["unit_in"])) or (
        unit_out not in list(df_temp["unit_out"])
    ):
        print(
            f"\tGet_Dict_Conv: either {unit_in} or {unit_out} not defined in configuration tables"
        )
        return {}
    elif unit_in == unit_out:
        if False:
            print("\tGet_Dict_Conv: units are equal, wasting time!")
        return dict_conv
    else:
        cond = df_temp.loc[:, ["unit_in", "unit_out"]] == [unit_in, unit_out]
        fcond = cond["unit_in"] & cond["unit_out"]
        conversion = df_temp.loc[fcond, :].reset_index(drop=True)

        # Make sure there is a match
        if conversion.shape != (1, 5):
            print(
                f"\tGet_Dict_Conv: no  conversion defined  for {unit_in} --> {unit_out}"
            )
            return {}
        else:
            dict_conv["bias"] = conversion.loc[0, "bias"]
            dict_conv["mult"] = conversion.loc[0, "mult"]

    return dict_conv


# ==========================================================================================
def Convert_x(x_in, unit_in, unit_out, PRJ):

    df_unitConvLin = PRJ.dict_config["UnitConvLin"].copy()
    dict_conv = Get_Dict_Conv(df_unitConvLin, unit_in, unit_out)
    if dict_conv == {}:
        print(f"No unit conversion defined for {unit_in}  to  {unit_out}")
        x_out = None
    else:
        x_out = (x_in + dict_conv["bias"]) * dict_conv["mult"]

    return x_out


# ==========================================================================================
def Convert_x_to_smpls(x_in, x_unit, PRJ, dso, always_odd=True):

    depth_unit = dso.df_varUnitInfo.loc["DEPTH", "unit_out"]
    sampRate_conv = Convert_x(dso.sampRate, depth_unit, depth_unit, PRJ)
    x_conv = Convert_x(x_in, x_unit, depth_unit, PRJ)

    # Conversion to samples
    X = round(x_conv / sampRate_conv)

    # if it has to be ODD
    if always_odd == True:
        if X % 2 == 0:
            X += 1

    return X
