import pandas as pd

from abner.Classes.Class_FileName import FileName

pd.set_option("future.no_silent_downcasting", True)


def Trim_Top_Bot_1W(PRJ, p_path, pars_input, dso):

    # Save incoming dso (original) to Diagnostics folder:
    dso.moduleName = FileName(__file__).justName
    dso.pars_input = pars_input.copy()
    if pars_input["saveDebug"]:
        dso.Save2Pck_Debug(str(p_path))

    # Book keeping
    df_misc = PRJ.dict_config["Misc"]
    vars_top = list(df_misc.loc["trim_logs_top", :])
    vars_bot = list(df_misc.loc["trim_logs_bot", :])

    vars_top = [s for s in vars_top if s == s]
    vars_bot = [s for s in vars_bot if s == s]

    # ENSURE THE LOGS EXIST
    set_vars_all = set(vars_top).union(set(vars_bot))
    hasVars = set_vars_all.issubset(set(dso.df_varUnitInfo["var_out"]))
    if hasVars == False:
        print(f"\tWell {p_path} can not be TRIMMED, all required logs do NOT exist")
    else:
        # Do they exist?
        idx_top = None
        idx_bot = None
        df = dso.df.copy()

        # Top business
        df_temp_top = df.dropna(axis=0, how="any", subset=vars_top, inplace=False)
        if len(df_temp_top) > 0:
            idx_top = df_temp_top.index[0]

        # Bottom business
        df_temp_bot = df.dropna(axis=0, how="any", subset=vars_bot, inplace=False)
        if len(df_temp_bot) > 0:
            idx_bot = df_temp_bot.index[-1]

        # Make sure idx_bot and idx_top exist, otherwise, leave them alone.
        if idx_top is None:
            print(f"\tTrim Top conditions not met for {p_path}")
            idx_top = dso.df.index[0]
        if idx_bot is None:
            print(f"\tTrim Bottom  conditions not met for {p_path}")
            idx_bot = dso.df.index[-1]

        # TRIM df in dso.df
        dso.df = dso.df.iloc[idx_top:idx_bot, :].copy()

        # HISTORY
    dso.UpdateHistory()

    # SAVE to pck
    if pars_input["save2pck"]:
        dso.Save2Pck(p_path)

    # MESSAGE
    print(f"Trimmed  well: {p_path}")

    return PRJ, dso
