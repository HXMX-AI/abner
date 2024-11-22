import pandas as pd
from copy import deepcopy


def LogDso_to_csv_1W(PRJ, p_path, dso):

    dso_out = deepcopy(dso)
    df_Misc = PRJ.dict_config["Misc"]
    temp = df_Misc.loc["csv_header_add", :]

    cols_add_temp = [s for s in temp if isinstance(s, str)]
    cols_add = [s for s in cols_add_temp if getattr(dso_out, s) is not None]

    for col in cols_add:
        x = pd.Series(getattr(dso_out, col), index=dso_out.df.index)
        dso_out.Add_Variable(x, col, "unitless")

    row_add = pd.DataFrame(columns=dso_out.df_varUnitInfo["var_out"], index=[0])
    row_add.iloc[0, :] = dso_out.df_varUnitInfo["unit_out"]

    df_out = pd.concat([row_add, dso_out.df], axis=0)

    p_out = (p_path.parent / "Output_Data" / p_path.stem).with_suffix(".csv")

    df_out.to_csv(p_out, index=False)

    return PRJ, dso
