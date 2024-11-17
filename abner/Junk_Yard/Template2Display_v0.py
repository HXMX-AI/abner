import  matplotlib.pyplot       as          plt
import  pandas                  as          pd
import  numpy                   as          np
from    Read_LAS_File           import      Read_LAS_File
from Junk_Yard.Class_FileName_NoStatic import      FileName
from    Get_Layout_Properties import      Get_Layout_Properties





#=.....................................................................................................................
def Template2Display(inputs):
    plt.rc('axes', edgecolor='black', linewidth = 0.5)

    props_tracks, props_logs, header_height = Get_Layout_Properties(inputs)
    df                                      = inputs['df_in']
    num_tracks                              = len(props_tracks)
    yLabelSize                              = inputs['gen_defaults']['yLabelSize']
    gridColor                               = inputs['gen_defaults']['gridColor']
    depth                                   = -1* df['DEPTH']


    # UPDATE DEPTH range for each track
    # def Adjust_Ylim(val):
    #     [axs[n].set_ylim(val) for n in range(layout.num_tracks)]
    #
    # # SCROLLER ==================================
    # def On_Scroll(event):
    #
    #     dz_event  = abs(slider.val[0]-slider.val[1])
    #     dz_scroll = dz_event * 0.250
    #     #dz_scroll = 20
    #     dz_min    = 10
    #     if event.button == 'up':
    #         zT_nxt = slider.val[1] + dz_scroll  # zT is always set to min(slider.valinit)
    #         if zT_nxt >= max(slider.valinit):
    #             zT_nxt = max(slider.valinit)
    #             zB_nxt = min(slider.val[0] + dz_scroll, zT_nxt - dz_min)
    #         else:
    #             zB_nxt = slider.val[0] + dz_scroll
    #     elif event.button == 'down':
    #         zB_nxt = slider.val[0] - dz_scroll
    #         if zB_nxt <= min(slider.valinit):
    #             zB_nxt = min(slider.valinit)
    #             zT_nxt = max(slider.val[1] - dz_scroll, zB_nxt + dz_min)
    #         else:
    #             zT_nxt = slider.val[1] - dz_scroll
    #     slider.set_val((zB_nxt, zT_nxt))
    #
    #
    #
    # CREATE the figure
    fig = plt.figure(figsize = (10, 5))

    # AXES  for TRACKS ..........................................................................
    axs = [None] * num_tracks * 2
    for n in range(num_tracks):
        coords_n = props_tracks[n]['coords'].tolist()
        axs[n]   = fig.add_axes(coords_n)
        axs[n].yaxis.set_tick_params(labelsize=yLabelSize)
        axs[n].xaxis.set_tick_params(labelsize=yLabelSize)
        axs[n].xaxis.set_tick_params(labelbottom=False)
        axs[n].grid(axis='both', linestyle='-', c=gridColor)

        # xticks
        xTicks = np.linspace(props_tracks[n]['xL'], props_tracks[n]['xR'], props_tracks[n]['nGrid']+1)
        axs[n].set_xticks(xTicks)
        axs[n].tick_params(direction='in')


        # Supress ylabels
        if n != 0:
            axs[n].tick_params(labelleft=False)
            axs[n].sharey(axs[0])

        # Logarithmic track
        if props_tracks[n]['xscale'] == 'log':
            axs[n].xaxis.set_tick_params(labelbottom=True)
            axs[n].set_xscale('log')
            axs[n].grid(which = 'minor')


    # # ADD the slider
    # bRow          = layout.df_coords.iloc[-1, :]
    # slider_coords = [bRow['xLeft'] + bRow['xLen']+0.01, bRow['yBot'], 0.03, bRow['yLen'] ]
    # depthRange    = (df_in.DEPTH.min(), df_in.DEPTH.max())
    # slider        = Add_Slider(fig, slider_coords, depthRange)
    #


    # LOGS ................................................................................
    for t in range(num_tracks):
        cond       = props_logs['trNum'] == t
        next_index = 0

        # GET log name
        xName = props_logs.loc[cond,:].index[next_index]
        x     = df[xName]

        # Plot logs, set xlim
        axs[t].plot(x, depth,
                    color     = props_logs.loc[xName,'color'],
                    linestyle =props_logs.loc[xName, 'style'],
                    linewidth = props_logs.loc[xName,'width'])
        axs[t].set_xlim( props_logs.loc[xName,['xL','xR']] )

        # If more than 1 log in the same track
        if sum(cond) > 1:
            next_index += 1
            xName   = props_logs.loc[cond,:].index[next_index]
            x       = df[xName]
            axs_add = axs[t].twiny()
            axs_add.plot(x, depth,
                    color     = props_logs.loc[xName,'color'],
                    linestyle = props_logs.loc[xName, 'style'],
                    linewidth = props_logs.loc[xName,'width'])
            axs_add.set_xlim( props_logs.loc[xName,['xL','xR']] )
            axs_add.set_xticks([])

            if props_tracks[t]['xscale'] == 'log':
                axs_add.set_xscale('log')
                axs_add.xaxis.set_tick_params(labeltop=False)

    # # ACTIVATE and SET
    # slider.on_changed(Adjust_Ylim)
    # fig.canvas.mpl_connect('scroll_event', On_Scroll)
    plt.show()

    return 'done'
















#======================================================================================================
if __name__ == "__main__":

    wd    = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
    fName = "15-9-19_SR_COMP.LAS"
    df_in = Read_LAS_File(wd, fName)


    templateFile       = "C:/Users/ridva/OneDrive/Documents/WELLS/" + "Log_Template_Volve.xlsx"
    df_template        = pd.read_excel(templateFile, sheet_name='Template')
    df_defaults        = pd.read_excel(templateFile, sheet_name='Defaults')
    gen_defaults       = pd.Series(df_defaults.Value)
    gen_defaults.index = df_defaults.Property
    fNameObj           = FileName(templateFile)

    inputs      = {
        'df_in':        df_in,
        'templateName': fNameObj.justName,
        'template':     df_template,
        'gen_defaults': gen_defaults
    }

    LayoutObj = Template2Display(inputs)

