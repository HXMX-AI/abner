import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from abner.Utilities.Read_LAS_File import Read_LAS_File
from abner.Classes.Class_FileName import FileName
from abner.Visualization.Get_Layout_Properties import Get_Layout_Properties
from matplotlib.lines import Line2D
from abner.Visualization.Add_Slider import Add_Slider
from matplotlib.backend_bases import MouseButton
import pickle


# ======================================================================================================================
def Make_LogPlot(inputs):
    plt.rc("axes", edgecolor="black", linewidth=0.5)

    # Check for f rotation
    if "rot" not in inputs["template"].columns:
        inputs["template"]["rot"] = "h"

    props_tracks, props_logs, header_height, max_header_rows = Get_Layout_Properties(
        inputs
    )
    df = inputs["df_in"]
    num_tracks = len(props_tracks)
    yLabelSize = inputs["gen_defaults"]["yLabelSize"]
    gridColor = inputs["gen_defaults"]["gridColor"]
    depth = -1 * df["DEPTH"]
    hdrLabelSize = inputs["gen_defaults"]["hdrLabelSize"]

    # UPDATE DEPTH range for each track
    def Adjust_Ylim(val):
        [axs[n].set_ylim(val) for n in range(num_tracks)]

    # SCROLLER ==================================
    def On_Scroll(event):

        dz_event = abs(slider.val[0] - slider.val[1])
        dz_scroll = dz_event * 0.250
        # dz_scroll = 20
        dz_min = 10
        if event.button == "up":
            zT_nxt = (
                slider.val[1] + dz_scroll
            )  # zT is always set to min(slider.valinit)
            if zT_nxt >= max(slider.valinit):
                zT_nxt = max(slider.valinit)
                zB_nxt = min(slider.val[0] + dz_scroll, zT_nxt - dz_min)
            else:
                zB_nxt = slider.val[0] + dz_scroll
        elif event.button == "down":
            zB_nxt = slider.val[0] - dz_scroll
            if zB_nxt <= min(slider.valinit):
                zB_nxt = min(slider.valinit)
                zT_nxt = max(slider.val[1] - dz_scroll, zB_nxt + dz_min)
            else:
                zT_nxt = slider.val[1] - dz_scroll
        slider.set_val((zB_nxt, zT_nxt))

        # ZOOM/MOOZ by MOUSE CLICK =.....................................................................

    def On_Click(event):
        lastPoint_x = event.xdata
        lastPoint_y = event.ydata

        # Avoid zooming on the slider, so that slider top/bot can move without jerking up or down
        if (lastPoint_x is None) | (lastPoint_x <= 1):
            return

        zBot = slider.val[0]
        zTop = slider.val[1]
        dz = abs(zTop - zBot)
        if event.button is MouseButton.LEFT:
            zBot = zBot - dz
            zTop = zTop + dz
            val_next = (zBot, zTop)
        elif event.button is MouseButton.RIGHT:
            zBot = zBot + (dz / 4)
            zTop = zTop - (dz / 4)
            val_next = (zBot, zTop)
        else:
            val_next = (zBot, zTop)
        slider.set_val(val_next)

    # CREATE the figure
    fig = plt.figure(figsize=(10, 5), num=inputs["fName"])

    # TRACKS ..........................................................................
    axs = [None] * num_tracks
    for n in range(num_tracks):
        coords_n = props_tracks[n]["coords"].tolist()
        axs[n] = fig.add_axes(coords_n)
        axs[n].yaxis.set_tick_params(labelsize=yLabelSize)
        axs[n].xaxis.set_tick_params(labelsize=yLabelSize)
        axs[n].xaxis.set_tick_params(labelbottom=False)
        axs[n].grid(axis="both", linestyle="-", c=gridColor)

        # xticks
        cond = props_logs["trNum"] == n
        xName = props_logs.loc[cond, :].index[0]
        xL, xR = props_logs.loc[xName, ["xL", "xR"]]
        xTicks = np.linspace(xL, xR, props_tracks[n]["nGrid"] + 1)
        axs[n].set_xticks(xTicks)
        axs[n].tick_params(direction="in")

        # Supress ylabels
        if n != 0:
            axs[n].tick_params(labelleft=False)
            axs[n].sharey(axs[0])

        # Logarithmic track
        if props_tracks[n]["xscale"] == "log":
            axs[n].xaxis.set_tick_params(labelbottom=True)
            axs[n].set_xscale("log")
            axs[n].grid(which="minor")

    # HEADER Tracks for logs ..............................................................................
    axs_hdr = [None] * num_tracks
    for n in range(num_tracks):
        coords_n = props_tracks[n]["coords"].tolist()
        newYBot = coords_n[1] + coords_n[-1]
        newYTop = 1.0 - newYBot
        coords_hdr = [coords_n[0], newYBot, coords_n[2], newYTop]
        axs_hdr[n] = fig.add_axes(coords_hdr)
        axs_hdr[n].set_xticks([])
        axs_hdr[n].set_yticks([])

    # MISSING LOGS in df? ....................................
    var_missing = []
    for var in props_logs.index:
        if var not in df.columns:
            df[var] = None
            var_missing.append(var)
            message = f"Variable {var}  is missing, will not be plotted"
            print(message)
            # Say_It(message, 200)

    # PLOT LOGS ................................................................................
    for t in range(num_tracks):
        cond = props_logs["trNum"] == t
        num_logs = sum(cond)
        next_index = 0

        # GET log name
        xName = props_logs.loc[cond, :].index[next_index]
        x = df[xName]

        # Plot logs, set xlim
        axs[t].plot(
            x,
            depth,
            color=props_logs.loc[xName, "color"],
            linestyle=props_logs.loc[xName, "style"],
            linewidth=props_logs.loc[xName, "width"],
        )

        if (pd.isna(props_logs.loc[xName, "shdTo"]) == False) and (
            xName not in var_missing
        ):
            axs[t].fill_betweenx(
                depth, x, color=props_logs.loc[xName, "shdClr"], alpha=1
            )

        axs[t].set_xlim(props_logs.loc[xName, ["xL", "xR"]])

        # If more than 1 log in the same track
        if num_logs > 1:
            for k in range(num_logs - 1):
                next_index += 1
                xName = props_logs.loc[cond, :].index[next_index]
                x = df[xName]
                axs_add = axs[t].twiny()
                axs_add.plot(
                    x,
                    depth,
                    color=props_logs.loc[xName, "color"],
                    linestyle=props_logs.loc[xName, "style"],
                    linewidth=props_logs.loc[xName, "width"],
                )

                if (pd.isna(props_logs.loc[xName, "shdTo"]) == False) and (
                    xName not in var_missing
                ):
                    axs[t].fill_betweenx(
                        depth, x, color=props_logs.loc[xName, "shdClr"], alpha=1
                    )

                axs_add.set_xlim(props_logs.loc[xName, ["xL", "xR"]])
                axs_add.set_xticks([])

                if props_tracks[t]["xscale"] == "log":
                    axs_add.set_xscale("log")
                    axs_add.xaxis.set_tick_params(labeltop=False)

    # COMPLETE the header section...................................................................
    yjump = 1 / max_header_rows
    y0 = yjump / 2
    for t in range(num_tracks):
        cond = props_logs["trNum"] == t
        num_logs = sum(cond)

        for n in range(num_logs):
            xName = props_logs.loc[cond, :].index[n]
            ycoord = 0.990 - (n + 1) * yjump + y0

            # ORIENTATION vertical or horizontal,
            hOrv = props_logs.loc[xName, "rot"]
            myRotation = "horizontal" if hOrv == "h" else "vertical"

            axs_hdr[t].text(
                0.5,
                ycoord,
                xName,
                rotation=myRotation,
                horizontalalignment="center",
                verticalalignment="center",
                color=props_logs.loc[xName, "color"],
                fontsize=hdrLabelSize,
            )

            if myRotation == "horizontal":
                xL = props_logs.loc[xName, "xL"]  # no need to wasting space for xx.0
                if xL == int(xL):
                    xL = int(xL)
                axs_hdr[t].text(
                    0.015,
                    ycoord,
                    xL,
                    horizontalalignment="left",
                    verticalalignment="center",
                    color=props_logs.loc[xName, "color"],
                    fontsize=hdrLabelSize,
                )

            if myRotation == "horizontal":
                xR = props_logs.loc[xName, "xR"]
                if xR == int(xR):
                    xR = int(xR)
                axs_hdr[t].text(
                    0.985,
                    ycoord,
                    xR,
                    horizontalalignment="right",
                    verticalalignment="center",
                    color=props_logs.loc[xName, "color"],
                    fontsize=hdrLabelSize,
                )

                line = Line2D(
                    [0.0, 1.0],
                    [ycoord - y0 / 2, ycoord - y0 / 2],
                    color=props_logs.loc[xName, "color"],
                    linewidth=props_logs.loc[xName, "width"],
                    linestyle=props_logs.loc[xName, "style"],
                )
                axs_hdr[t].add_line(line)

    # """

    # ADD the slider
    bRow = props_tracks[-1]["coords"]
    slider_coords = [
        bRow["xLeft"] + bRow["xLen"] + 0.01,
        bRow["yBot"],
        0.03,
        bRow["yLen"],
    ]
    depthRange = (depth.min(), depth.max())
    slider = Add_Slider(fig, slider_coords, depthRange)

    # ACTIVATE and SET
    slider.on_changed(Adjust_Ylim)
    fig.canvas.mpl_connect("scroll_event", On_Scroll)
    fig.canvas.mpl_connect("button_press_event", On_Click)

    plt.show()

    return "done"


# ======================================================================================================
if __name__ == "__main__":

    inputFileType = "today"

    match inputFileType:

        case "las":
            wd = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
            fName = "15-9-19_SR_COMP.LAS"
            _, df_in = Read_LAS_File(wd, fName)
            if "DEPTH" not in df_in.columns:
                df_in["DEPTH"] = df_in.index

        case "pck":
            wd = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
            fNames = [
                "15-9-19_SR_COMP.pck",
                "15_9-F-1A.pck",
                "15_9-F-1B.pck",
                "15_9-F-1C.pck",
                "15_9-F-11A.pck",
                "15_9-F-11B.pck",
            ]
            fName = fNames[5]
            with open(wd + fName, "rb") as file:
                LogDs = pickle.load(file)
            df_in = LogDs.df

        case "today":
            wd = "C:/Users/ridva/OneDrive/Documents/WELLS/A_Mix_Format/"
            fNames = ["Well_2A.pck", "Well_2A.pck", "15-9-19_SR_COMP.pck"]  #

            # wd     = "C:/Users/ridva/OneDrive/Documents/WELLS/HexMex/"
            # fNames = ["33053015380000_NELSON 81_1.pck",
            #           "33053015560000_LINDVIG DAVIDSON A_1.pck",
            #           "33053017790000_FJELSTAD_6-3.pck"]

            fName = fNames[2]
            with open(wd + fName, "rb") as file:
                LogDs = pickle.load(file)
            df_in = LogDs.df

    templateFile = "C:/Users/ridva/OneDrive/Documents/WELLS/" + "Log_Template_HXMX.xlsx"
    df_template = pd.read_excel(templateFile, sheet_name="Template")
    df_defaults = pd.read_excel(templateFile, sheet_name="Defaults")
    gen_defaults = pd.Series(df_defaults.Value)
    gen_defaults.index = df_defaults.Property
    fNameObj = FileName(templateFile)

    inputs = {
        "fName": fName,
        "df_in": df_in,
        "templateName": fNameObj.justName,
        "template": df_template,
        "gen_defaults": gen_defaults,
    }

    status = Make_LogPlot(inputs)
