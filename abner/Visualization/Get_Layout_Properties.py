import pandas as pd


def Get_Layout_Properties(inputs):

    template = inputs["template"]
    xMargin = inputs["gen_defaults"]["xMargin"]
    yMargin = inputs["gen_defaults"]["yMargin"]
    yHeader = inputs["gen_defaults"]["yHeader"]

    # KEEP only the rows that are to be shown ........................
    template = template[template["show"] != 0].copy()

    # SET num_tracks, num_logs .......................................
    track_nums = template["trNum"].unique()
    track_nums.sort()
    num_tracks = len(track_nums)
    num_logs = template.shape[0]

    # SORT  Tracks and create index ...................................
    template.sort_values(by=["trNum"], inplace=True)
    template.index = range(template.shape[0])

    # ADJUST track Numbers modified .........................................
    org_to_new = pd.Series(range(num_tracks), index=track_nums)
    for n in range(num_logs):
        template.loc[n, "trNum"] = org_to_new[template.loc[n, "trNum"]]

    # SET Track lengths ...................................................
    tr_len = []
    logs_per_track = []
    sum_tr_len = 0
    for n in range(num_tracks):
        cond = template.trNum == n
        temp = template.loc[cond, "trLen"]
        tr_len.append(temp.max())
        logs_per_track.append(len(temp))
        sum_tr_len = sum_tr_len + tr_len[n]

    # SET Scaler for adjusting to track lengths and xMargin .............
    scaler = (1 - 2 * xMargin) / sum_tr_len

    # SET xlen for each track ...............................................
    tr_xlen = [temp * scaler for temp in tr_len].copy()

    # SET ylen for each track
    max_header_rows = max(logs_per_track)
    header_height = max_header_rows * yHeader
    tr_ylen = 1.0 - (2 * yMargin) - header_height  # was yHeader

    # SET Coordinates for all axes .......................................................................
    df_coords = pd.DataFrame(
        columns=["xLeft", "yBot", "xLen", "yLen"], index=range(num_tracks)
    )
    df_coords["xLen"] = tr_xlen.copy()
    df_coords["yBot"] = yMargin
    df_coords["yLen"] = tr_ylen

    # SET xL, xR for all tracks ....................................................
    xRight_last = xMargin
    xL = []
    xR = []
    for n in range(num_tracks):
        xL.append(xRight_last)
        xR.append(xL[n] + tr_xlen[n])
        xRight_last = xR[n]

    # SET xLeft
    df_coords["xLeft"] = xL.copy()

    # CREATE tracks .................................................................
    props_tracks = []
    for t in range(num_tracks):
        props = {}
        props["number"] = t
        props["coords"] = df_coords.iloc[t, :]

        cond = template.trNum == t
        props["logNames"] = template.loc[cond, "logName"]
        props["logs_per_track"] = len(props["logNames"])

        if sum(template.loc[cond, "logScale"]) >= 1:
            props["xscale"] = "log"
        else:
            props["xscale"] = "linear"

        # TO handle MULTIPLE logs per track
        props["xL"] = min(template.loc[cond, "xL"])
        props["xR"] = max(template.loc[cond, "xR"])
        props["nGrid"] = max(template.loc[cond, "nGrid"])

        props_tracks.append(props)

    # SET props_logs ..................................................................
    cols = [
        "trNum",
        "xL",
        "xR",
        "color",
        "style",
        "width",
        "inHdr",
        "shdTo",
        "shdClr",
        "rot",
    ]
    props_logs = template.loc[:, cols].copy()
    props_logs.index = template["logName"]

    return props_tracks, props_logs, header_height, max_header_rows
