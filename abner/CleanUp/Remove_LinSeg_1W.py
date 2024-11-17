import  pandas                      as              pd
from    Classes.Class_FileName      import          FileName
from    Utilities.Functions_Units   import          Convert_x_to_smpls
import  numpy                       as              np
# from    scipy                       import          stats
from    scipy.stats                 import          zscore
import  matplotlib.pyplot           as              plt
from    Utilities.Say_It            import          Say_It
pd.set_option('future.no_silent_downcasting', True)


#======================================================================================
def Remove_LinSeg_1W(PRJ, p_path, pars_input, dso):

    dso.moduleName = FileName(__file__).justName
    dso.pars_input = pars_input.copy()
    if pars_input['saveDebug']:
        dso.Save2Pck_Debug(str(p_path))


    # Book keeping
    df_linSeg   = PRJ.dict_config['LinSeg']
    df_harm     = PRJ.dict_config['Harmonization']

    # Operate on only those defined in Harmonization tables
    set_varList_def = set(dso.df_varUnitInfo['var_out']).intersection(set(df_harm.index))
    var_special     = set_varList_def.intersection(set(df_linSeg.index))
    var_temp        = df_linSeg.loc['takeLog',:]
    var_take_log    = set(var_temp).intersection(set(dso.df_varUnitInfo['var_out']))

    # ADJUSt the variance df for the special cases
    df_variance           = pd.DataFrame(columns = ['maxVar'], index = list(set_varList_def))
    df_variance['maxVar'] = df_linSeg.loc['variance_all',:].iloc[0]
    for v in var_special:
        df_variance.loc[v,'maxVar'] = df_linSeg.loc[v,:].iloc[0]

    # PROCESS only those with maxVar > 0
    mask        = df_variance['maxVar'] != 0
    df_variance = df_variance[mask].copy()
    set_varList_def = set_varList_def.intersection(set(df_variance.index))

   # TERMINATE early if nothing to process
    if len(set_varList_def) == 0:
        print(f'Remove_LinSeg_1W: {p_path.stem}, no data to process')
        return PRJ, dso

    # Obtain wLen and padLen in smpls
    wLen, wLen_unit     = df_linSeg.loc['wLen'].iloc[:2]
    wLen_smpls          = Convert_x_to_smpls(wLen, wLen_unit, PRJ, dso,  always_odd = True)
    padLen, padLen_unit = df_linSeg.loc['padLen'].iloc[:2]
    if padLen_unit != 'smpls':
        padLen_smpls = Convert_x_to_smpls(padLen, padLen_unit, PRJ, dso, always_odd = True)
    else:
        padLen_smpls = padLen


    # df_temp CREATE
    df_temp = dso.df.loc[:,list(set_varList_def)].copy()

    # Log(var) if there is takeLog
    #var_take_log = df_linSeg.loc['takeLog']
    for var in var_take_log:
        df_temp.loc[:,var] = np.log10(df_temp[var]).copy()


    # ZSCORE: STANDARDIZATION ...................................................................................................

    if df_linSeg.loc['zScore'].iloc[0] == 1:
        df_temp = df_temp.apply(lambda x: zscore(x, nan_policy='omit'))

    # Variance
    df_temp_diff = df_temp.diff()  # was axis = 0
    df_roll      = df_temp_diff.rolling(window=wLen_smpls, min_periods=1, center=True, win_type=None, closed=None).var()

    # Create variance matrix
    df_flag = pd.DataFrame(0, columns = df_temp.columns, index = df_temp.index, dtype=bool)
    for v in df_temp.columns:
        cond = df_roll.loc[:,v] < df_variance.loc[v,'maxVar']
        df_flag.loc[:,v] = cond

    # Convert to integers, needed for padding
    df_flag = df_flag.replace({True: 1, False: 0})

    # Convolve to extend the flag since it is the center
    df_flag = df_flag.rolling(window=wLen_smpls, min_periods=1, center=True, win_type=None, closed=None).max()

    # Pad if needed
    if padLen_smpls > 0:
        df_flag = df_flag.rolling(window=padLen_smpls, min_periods=padLen_smpls//2, center=True, win_type=None, closed=None).max()

    # Null those data points, if asked for
    if df_linSeg.loc['remove_linSegs'].iloc[0] == True:
        dso.df.mask(df_flag.astype('bool'), other=None, inplace=True)
    else:
        #Say_It('Remove Linear segments is turned OFF')
        print('Remove Linear segments is turned OFF')

    # Composite flag for the entire dataframe
    FL_LINSEG              = df_flag.max(axis=1)

    # Update FL_LINSEG
    dso.Add_Variable(FL_LINSEG, 'FL_LINSEG', "unitless")

    # SAve for debugging, if asked for
    if df_linSeg.loc['save_df_linSeg',:].iloc[0] == True:
        df_flag['FL_LINSEG'] = FL_LINSEG.copy()
        dso.df_linSeg        = df_flag.copy()

        # HISTORY
    dso.UpdateHistory()

    # SAVE to pck
    if pars_input['save2pck']:
        dso.Save2Pck(p_path)

    # MESSAGE
    if df_linSeg.loc['remove_linSegs',:].iloc[0] == True:
        print(f'Removed linSegs  well: {p_path}')
    else:
        print(f'Ran Remove_LinSeg_1W on {p_path}')


    return PRJ, dso



#-------------------------------------------------------------------------
if __name__ == "__main__":
    pass