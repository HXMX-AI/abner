import  pickle
from    abner.Utilities.FilesInDir        import      FilesInDir
from    pathlib                     import      Path
from    abner.Utilities.Say_It            import      Say_It

#=======================================================================================================================
def Depth_Check_1W(PRJ, p_path, pars_input, dso):

    dso.moduleName = Path(__file__).stem
    dso.pars_input = pars_input.copy()
    if pars_input['saveDebug']:
        dso.Save2Pck_Debug(str(p_path))

    depth_inc_tol  = 1e-09
    df_misc        = PRJ.dict_config['Misc']

    downLog_flip        = df_misc.loc['depth_downLog_flip',:].iloc[0]
    drop_negative_depth = df_misc.loc['depth_drop_negative_depth',:].iloc[0]

    orgSampRate     = dso.dict_depthInfo['orgSampRate']
    sampRate        = dso.dict_depthInfo['sampRate']


    # To get a positive sampling rate for logging up, periods should be set to 1.
    depth_diff      = dso.df['DEPTH'].diff(periods= 1)
    sampRate_mean   = depth_diff.iloc[:-1].mean()
    sampRate_medi   = depth_diff.iloc[:-1].median()


    # If mean and medi sampling rates computed from data are within the tolerance, go with the mean.
    if abs(sampRate_mean - sampRate_medi) <= depth_inc_tol:
        sampRate_meas = sampRate_mean

    # If no sampRate, i.e., a csv file, then set both orgSampRate and sampRate
    # elif measured vs recorded sampRate are within the tolerance, no need to change, i.e., pass
    # elif measured vs recorded sampRates are so different, change it to sampRate_meas, i.e, trust own calculation
    if sampRate is None:
        dso.Update_SampRate(sampRate_meas, sampRate_meas)
    elif (sampRate_meas - sampRate)  <=  depth_inc_tol:
        pass                                                        # for clearer logic
    elif abs(sampRate_meas - sampRate)  >  depth_inc_tol:  # Compare to the incoming sampRate
        Say_It(f' Mismatch:  header versus computed sampling rates are different ')
        print(f'{p_path=}')
        print(f'well {dso.wellName} resetting sampling rate to {sampRate} to {sampRate_meas}')
        sampRate = sampRate_meas
        dso.Update_SampRate(sampRate_meas)


    # Check for UpLog (NORMAL) or DOWNLOG (not normal)
    if dso.sampRate < 0:
        Say_It('You have a down log')
        print(f'{dso.wellName} in {p_path} is a down log')

        if downLog_flip:
            sampRate   = -1 * sampRate
            dso.Update_SampRate(sampRate)
            dso.df     = dso.df.iloc[::-1].reset_index(drop=True).copy()
            depth_diff = dso.df['DEPTH'].diff(periods=1)
            print(f'Flipping depth')
        else:
            Say_It('Are you sure you do not want to flip down logs?')

    # Check for NEGATIVE depths
    cond = dso.df['DEPTH'] < 0
    if cond.sum() > 0:
        print(f'You have negative depths')
        if drop_negative_depth:
            cond   = dso.df['DEPTH'] >= 0
            dso.df = dso.df.loc[cond, :].copy()
            dso.df = dso.df.reset_index(drop = True)

    # Check for NULLS in depth
    null_count = dso.df['DEPTH'].isna().sum()
    if null_count > 0:
        print(f'{p_path} has {null_count} nulls')
        Say_It('Null DEPTH values are detected')
        dso.dict_depthInfo['numNulls'] = null_count
        if drop_negative_depth:
            dso.df.dropna(axis=0, how= 'any', subset=['DEPTH'], inplace=True, ignore_index=True)
    else:
        dso.dict_depthInfo['numNulls'] = 0



    # Check for depth reversal (yoyo)
    cond = depth_diff[:-1] < 0
    if cond.any(skipna = False):
        dso.dict_depthInfo['hasReversal'] = True
        print(f'{cond.sum()} depth points are reversed')
    else:
        dso.dict_depthInfo['hasReversal'] = False

    # Check for gaps in depth
    cond = depth_diff[:-1].abs() >= 1.75 * dso.dict_depthInfo['sampRate']
    if cond.any():
        dso.dict_depthInfo['hasGaps'] = True
    else:
        dso.dict_depthInfo['hasGaps'] = False




    # HISTORY
    dso.UpdateHistory()

    # SAVE
    if pars_input['save2pck'] :
        dso.Save2Pck(p_path)
    if True: print(f'Checked DEPTH in   well: {dso.wellName}')

    return PRJ, dso



#=========================================================================
if __name__ == '__main__':



    # INPUT pck files
    dir_prj      = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
    fileNames    = FilesInDir(dir_prj)

    for pckFileName in fileNames:
        with open(pckFileName, 'rb') as file:
            dso = pickle.load(file)

        # pars_input
        pars_input                 = {}
        pars_input['pckFileName']  = pckFileName
        pars_input['save2pck']     = True
        pars_input['saveDebug']    = True
        new_dso                    = Depth_Check_1W(pars_input, dso)


    print('done')