import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from time import process_time

from abner.Utilities.Functions_Units import Convert_x, Convert_x_to_smpls


def MakePlot(w, x, y, z, wellName=""):
    _, ax = plt.subplots(2, 1, sharex=True)

    plt.suptitle(wellName)

    n = 0
    ax[n].plot(z, w, "b")
    ax[n].plot(z, x, "r.")
    ax[n].grid(axis="y")
    ax[n].grid(axis="x")

    n = 1
    ax[n].plot(z, w, "b")
    ax[n].plot(z, y, "r.")
    ax[n].grid(axis="both")

    plt.show()


def Get_Max_Diff(PRJ, bitsize):

    # creates the threshold which will be used to determine a flag frm the differential caliper
    df_borehole = PRJ.dict_config["BoreHole"].copy()
    method = df_borehole.loc["fl_dcal_method", 1]
    max_by_in = df_borehole.loc["fl_dcal_by_in_max", 1]
    max_by_pr = df_borehole.loc["fl_dcal_by_pr_max", 1]

    match method:
        case "by_in":
            max_diff = max_by_in
        case "by_pr":
            max_diff = bitsize * (max_by_pr / 100)
        case _:
            print("Create_Flag_DCAL: your method {method}  is NOT recognized")
            return None

    return max_diff


def Compute_DCAL(PRJ, dso):

    bs = dso.df["BS"].copy()
    cali = dso.df["CALI"].copy()
    max_diff = Get_Max_Diff(PRJ, bs)

    DCAL = cali - bs
    FL_DCAL = pd.Series(0.0, index=bs.index)
    cond = DCAL >= max_diff
    FL_DCAL[cond] = 1.0

    # Updates for new variables
    dso.Add_Variable(DCAL, "DCAL", dso.df_varUnitInfo.loc["CALI", "unit_out"])
    dso.Add_Variable(FL_DCAL, "FL_DCAL", "unitless")

    return dso


def Compute_Pseu_DCAL(PRJ, dso):
    df_borehole = PRJ.dict_config["BoreHole"]
    wLen_Min, wLen_Min_unit = df_borehole.loc["pseudo_bs_wLenMin"][1:3]
    wLen_Max, wLen_Max_unit = df_borehole.loc["pseudo_bs_wLenMax"][1:3]

    cond = dso.df["CALI"].notna()
    cali = dso.df["CALI"][cond].copy()
    zzzz = dso.df["DEPTH"][cond].copy()

    wLen_Min_conv = Convert_x(
        wLen_Min, wLen_Min_unit, dso.df_varUnitInfo.loc["DEPTH", "unit_out"], PRJ
    )
    wLen_Max_conv = Convert_x(
        wLen_Max, wLen_Max_unit, dso.df_varUnitInfo.loc["DEPTH", "unit_out"], PRJ
    )

    nMin = int(wLen_Min_conv / dso.sampRate)
    if nMin % 2 == 0:
        nMin += 1

    nMax = int(wLen_Max_conv / dso.sampRate)
    if nMax % 2 == 0:
        nMax += 1

    # INITIALIZE cali_min_full to zero - only if it is a number (skipping nans)
    cali_min_full = pd.Series(0.0, index=cali.index, name="cali_min_full")

    cali_max = cali.rolling(
        nMax, min_periods=nMax, center=True, win_type=None, step=1
    ).max()
    cali_min_step = cali_max.rolling(
        nMin, min_periods=1, center=True, win_type=None, step=nMin // 2
    ).min()

    for i in range(len(cali_min_step.index) - 1):
        idx_beg = cali_min_step.index[i]
        idx_end = min(cali_min_step.index[i + 1], cali_min_full.index[-1])
        # Convert to integers for indexing
        mask = (cali_min_full.index >= idx_beg) & (cali_min_full.index <= idx_end)
        cali_min_full[mask] = cali_min_step[idx_beg]
    # the last leg
    mask = cali_min_full.index >= idx_end
    cali_min_full[mask] = cali_min_step[cali_min_step.index[-1]]

    BS_PSEU = cali_min_full.rolling(
        nMax, min_periods=1, center=True, win_type=None
    ).min()
    max_diff = Get_Max_Diff(PRJ, BS_PSEU)
    DCAL_PSEU = cali - BS_PSEU
    FL_DCAL_PSEU = pd.Series(0.0, index=BS_PSEU.index)
    cond = DCAL_PSEU >= max_diff
    FL_DCAL_PSEU[cond] = 1.0

    # Just to PLOT
    if False:
        MakePlot(cali, BS_PSEU, FL_DCAL_PSEU, zzzz, dso.wellName)

    # Updates for new variables
    dso.Add_Variable(BS_PSEU, "BS_PSEU", dso.df_varUnitInfo.loc["DEPTH", "unit_out"])
    dso.Add_Variable(DCAL_PSEU, "DCAL_PSEU", dso.df_varUnitInfo.loc["CALI", "unit_out"])
    dso.Add_Variable(FL_DCAL_PSEU, "FL_DCAL_PSEU", "unitless")

    return dso


def Compute_Mud_Signal(PRJ, dso):

    # zart, zurt = Compute_Mud_Signal_OLD(PRJ, dso)

    t1_start = process_time()
    assert dso.df_varUnitInfo.loc["CALI", "unit_out"] == "in", print(
        "BoreholeComputations_Mud_Signal CALI not in inches"
    )

    df_borehole = PRJ.dict_config["BoreHole"]
    padLen, padLen_unit = df_borehole.loc["mudS_padLength"][1:3]
    vertRes, vertRes_unit = df_borehole.loc["mudS_vertRes"][1:3]
    standOff, standOff_unit = df_borehole.loc["mudS_standOff"][1:3]
    doi, doi_unit = df_borehole.loc["mudS_doi"][1:]
    max_diff = df_borehole.loc["mudS_max_diff"][1]

    depth_unit = dso.df_varUnitInfo.loc["DEPTH", "unit_out"]
    sampRate_conv = Convert_x(dso.sampRate, depth_unit, "in", PRJ)
    vertRes_conv = Convert_x(vertRes, vertRes_unit, "in", PRJ)
    standoff_conv = Convert_x(standOff, standOff_unit, "in", PRJ)
    doi_conv = Convert_x(doi, doi_unit, "in", PRJ)

    if vertRes_conv is None or standoff_conv is None or doi_conv is None:
        print("BoreholeComputations_Mud_Signal: some conversions failed")
        return dso

    Area = (vertRes_conv + sampRate_conv) * (doi_conv - standoff_conv)

    padLen_smpls = Convert_x_to_smpls(padLen, padLen_unit, PRJ, dso, always_odd=True)
    vertRes_smpls = Convert_x_to_smpls(vertRes, vertRes_unit, PRJ, dso, always_odd=True)
    cali = dso.df["CALI"].copy()
    Area = (vertRes_smpls) * (
        doi_conv - standoff_conv
    )  # not true area, skipping sampRate

    # Repeated df - CREATE
    numCols = len(cali.index)
    df_temp = pd.DataFrame(np.zeros((padLen_smpls + 1, numCols), dtype=float))
    for n in range(padLen_smpls):
        df_temp.iloc[n, n:] = cali[0 : numCols - n]

    # Take min for calculating tool position
    df_temp.iloc[padLen_smpls, :] = df_temp.iloc[0:padLen_smpls, :].min(axis=0)

    # Subtract the minimum from the df
    df_temp.iloc[:padLen_smpls, :] = (
        df_temp.iloc[:padLen_smpls, :] - df_temp.iloc[padLen_smpls, :]
    ).copy()

    # Check for readings greater than doi
    cond = df_temp > doi_conv
    df_temp[cond] = doi_conv

    # Check for reading less than standoff
    cond = df_temp < standoff_conv
    df_temp[cond] = standoff_conv

    # MUD SIGNAL
    i0 = (padLen_smpls - vertRes_smpls) // 2
    i1 = i0 + vertRes_smpls
    df_temp.iloc[padLen_smpls, :] = df_temp.iloc[i0:i1].sum(axis=0)

    j0 = vertRes_smpls - 1
    j1 = len(cali.index) - vertRes_smpls
    mud_sgnl = pd.Series(0.0, index=cali.index)
    unshifted_mud_sgnl = (
        df_temp.iloc[padLen_smpls, :] - (vertRes_smpls * standoff_conv)
    ) / Area

    # Fix the length mismatch by using the same range for both sides
    mud_sgnl.iloc[j0:j1] = unshifted_mud_sgnl.iloc[
        padLen_smpls - 1 : -(padLen_smpls - 1)
    ]

    FL_MUD_SGNL = pd.Series(0.0, index=dso.df["CALI"].index)
    cond = mud_sgnl >= max_diff
    FL_MUD_SGNL[cond] = 1.0

    # Updates for new variables
    dso.Add_Variable(max_diff, "MUD_SGNL_MAX", "unitless")
    dso.Add_Variable(mud_sgnl, "MUD_SGNL", "unitless")
    dso.Add_Variable(FL_MUD_SGNL, "FL_MUD_SGNL", "unitless")

    t1_stop = process_time()
    print(f"{dso.wellName:}, elapsed time: {t1_stop - t1_start}\n\n")

    return dso
