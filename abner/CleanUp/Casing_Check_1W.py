import  pandas                      as              pd
from    abner.Classes.Class_FileName      import          FileName
from    abner.Utilities.Functions_Units   import          Convert_x_to_smpls
import  numpy                       as              np
import  matplotlib.pyplot           as              plt
pd.set_option('future.no_silent_downcasting', True)




#======================================================================================
def Casing_Check_1W(PRJ, p_path, pars_input, dso):

    # Save incoming dso (original) to Diagnostics folder:
    dso.moduleName = FileName(__file__).justName
    dso.pars_input = pars_input.copy()
    if pars_input['saveDebug']:
        dso.Save2Pck_Debug(str(p_path))

    if 'DTCO' not in dso.df_varUnitInfo['var_out']:
        print(f'\tNo Casing Check: well {p_path} does not have DTCO, skipping the process')
        flag_final = pd.Series(None, index = dso.df.index)

    else:
        # Book keeping
        df_misc              = PRJ.dict_config['Misc']
        specs                = list(df_misc.loc['casing_dtco',:])
        specs                = [s for s in specs if s == s]

        # GET SPECS
        dt_casing_mean       = specs[0]
        dt_casing_del        = specs[1]
        dt_casing_unit       = specs[2]
        dt_casing_thick      = specs[3]
        dt_casing_thick_unit = specs[4]


        # CHECKS and CONVERSIONS
        if (dt_casing_unit != 'us/ft') or (dt_casing_mean != 57.0):
            print('Casing_Check: Out of range Specs')
            print(f'Casing dt must be:  {dt_casing_mean}, dtco unit must be us/ft')
            print(f'Currently: {dt_casing_mean=}, {dt_casing_std=}')

        # CALCULATE
        wLen_smpls   = Convert_x_to_smpls(dt_casing_thick, dt_casing_thick_unit, PRJ, dso,  always_odd = True)
        dt           = dso.df['DTCO'].copy()

        # flag_in: a value is in the desired dt window
        dt_min        = dt_casing_mean - dt_casing_del
        dt_max        = dt_casing_mean + dt_casing_del
        flag_in       = pd.Series(0, index = dt.index)
        cond          = dt.between(dt_min, dt_max, inclusive = "both" )
        flag_in[cond] = 1

        # Make sure that there are at lest wLen_smpls of 1s consecutively
        dt_roll_min   = pd.Series(0, index = dt.index)
        dt_roll_min   = flag_in.rolling(window=wLen_smpls, min_periods=1, center=False).min()


        N             = len(dt)
        df_temp       = pd.DataFrame(np.zeros((wLen_smpls+2, N)))
        for i in range(wLen_smpls):
            df_temp.iloc[i, :N - i] = dt_roll_min[i:N]

        df_temp.iloc[wLen_smpls, :] = df_temp.iloc[:wLen_smpls, :].max(axis=0)
        flag_final = df_temp.iloc[wLen_smpls, :] >= 1
        flag_final = flag_final.astype(int)

        if False:
            Plot_Debug(dt, dso.df.DEPTH, flag_in, dt_roll_min, flag_final)


    dso.Add_Variable(flag_final, 'FL_CASING', "unitless")


        # HISTORY
    dso.UpdateHistory()

    # SAVE to pck
    if pars_input['save2pck']:
        dso.Save2Pck(p_path)

    # MESSAGE
    print(f'Checked for Casing  {p_path}')



    return PRJ, dso


# ======================================================================================
def Plot_Debug(dt, z, flag_in, dt_roll_min, flag_final):
    xLim = [40, 140]

    # SET FIGURE
    fig, ax = plt.subplots(nrows=1, ncols=4, sharey=True)
    ax[0].plot(dt,  z, 'k.')
    ax[0].set_xlim(xLim)
    ax[0].grid()
    ax[0].set_title('dt')

    ax[1].plot(flag_in, z, 'r+', markersize=3)
    ax[1].set_xlim(-0.1, 1.1)
    ax[1].grid()
    ax[1].set_title('flag-in')

    ax[2].plot(dt_roll_min, z, 'r+', markersize=3)
    ax[2].set_xlim(-2, 2)
    ax[2].grid()
    ax[2].set_title('dt_roll_min')

    n = 3
    ax[n].plot(flag_final, z, 'ro', markersize=1)
    ax[n].set_xlim(0, 2)
    ax[n].grid()

    plt.show()




#-------------------------------------------------------------------------
if __name__ == "__main__":
    pass