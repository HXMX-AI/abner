import      pandas                              as              pd
import      pickle
import      lasio
from        Class_LogDataSet                    import          LogDataSet
import      numpy                               as              np
from        Class_FileName                      import          FileName
from        pathlib                             import          Path
from        Utilities.Functions_Units           import          Get_Units_Recognized, Get_Depth_Variable_Unit, Get_Dict_DepthInfo
from        Utilities.Functions_Misc            import          BitSize_Convert


#=======================================================================================================================
def LAS_to_LogDataSet_1W(PRJ, path_file, pars_input):

    print(f'{Path(__file__).stem} processing well: {path_file.stem}')
    las                  = lasio.read(path_file)
    LogDs                = LogDataSet()

    LogDs.format_in                  = 'LAS'
    LogDs.fileName                   = path_file.stem
    LogDs.wellName                   = las.well.WELL.value
    LogDs.datasetName                = 'INPUTLAS'
    LogDs.nullValue                  = las.well.NULL.value
    LogDs.sampRate                   = las.well.STEP.value
    LogDs.API                        = las.well.API.value       if 'API' in las.well else None
    LogDs.orgAPI                     = LogDs.API
    LogDs.UWI                        = las.well.UWI.value       if 'UWI' in las.well else None
    LogDs.Xcoord                     = las.well.XCOORD.value    if 'XCOORD' in las.well else None
    LogDs.Ycoord                     = las.well.YCOORD          if 'YCOORD' in las.well else None
    LogDs.LAT                        = las.well.LAT.value       if 'LAT' in las.well else None
    LogDs.LON                        = las.well.LON.value       if 'LON' in las.well else None
    LogDs.pars_input                 = pars_input
    LogDs.moduleName                 = FileName(__file__).justName

    varList   = [s.mnemonic for s in las.curves]
    unitList  = [s.unit for s in las.curves]


    # API Check
    if LogDs.API is not None:
        if '-' in LogDs.API:
            LogDs.API = LogDs.API.replace('-','')

        if len(LogDs.API) ==  10:
            LogDs.API = LogDs.API+'0000'


    # BS check and add
    if ('BS' in las.params) and (las.params.BS.value is not None):
        has_BS = True
        temp_bs = las.params.BS.value
    else:
        has_BS = False

    if has_BS:
        bs      = BitSize_Convert(str(temp_bs))
        varList.append('BS')
        unitList.append(las.params.BS.unit)



    # Depth related stuff
    dictUnit, dictUnit_in, depthName_in, depthUnit = Get_Dict_DepthInfo(varList, unitList, PRJ.dict_config)
    LogDs.dict_depthInfo['depthName_in'] = depthName_in
    LogDs.dict_depthInfo['depthName']    = depthName_in
    LogDs.dict_depthInfo['depthUnit']    = depthUnit


    LogDs.df_varUnitInfo['var_in']    = dictUnit.keys()
    LogDs.df_varUnitInfo['var_out']   = dictUnit.keys()
    LogDs.df_varUnitInfo['unit_in']   = dictUnit.values()
    LogDs.df_varUnitInfo['unit_out']  = [s.casefold() for s in dictUnit.values()]
    LogDs.df_varUnitInfo['unitValid'] = None
    LogDs.df_varUnitInfo.index        = dictUnit.keys()

    # Setting both orgSampRate and sampRate at creation
    LogDs.Update_SampRate(LogDs.sampRate, LogDs.sampRate)


    # Creating the dataframe for log data
    temp       = las.df()
    if has_BS:
        temp['BS'] = bs
    colNames   = temp.columns
    numRows    = temp.shape[0]
    df         = pd.DataFrame(columns = varList, index = range(numRows))

    df[colNames]     = np.array(temp[colNames])
    df[depthName_in] = temp.index




    # If the depth variable is not called DEPTH, make necessary changes to df
    df.rename(columns = {depthName_in: 'DEPTH'}, inplace = True)
    LogDs.df = df

    # Update history
    LogDs.UpdateHistory()

    # Save the LogDs object to a pickle file in the Input_Data folder, as well as in dir_prj
    if pars_input['save2pck'] == True:

        suf     = 'log.pck'
        the_suf = f"{path_file.stem}.{suf}"
        pckName_out  = PRJ.dir_prj / "Input_Data" / the_suf
        LogDs.Save2Pck(pckName_out)
        #
        pckName_in      = PRJ.dir_prj / the_suf
        LogDs.Save2Pck(pckName_in)

    return LogDs


#==============================================================
if __name__ == "__main__":

    dir_prj = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
    dir_in  = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/Input_Data/"
    dir_out = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
    fNames = ["15-9-19_SR_COMP.las",
              "15_9-F-1A.LAS",
              "15_9-F-1B.LAS",
              "15_9-F-1C.LAS",
              "15_9-F-11A.LAS",
              "15_9-F-11B.LAS",
              ]

    for i in range(len(fNames)):
        pars_input             = {}
        pars_input['dir_prj']  = dir_prj
        pars_input['dir_in']   = dir_in
        pars_input['dir_out']  = dir_out
        pars_input['fName']    = fNames[i]
        pars_input['save2pck'] = True

        newObj =  LAS_to_LogDataSet_1W((pars_input))
        print(f' converted  {fNames[i]}')

    print(f'Finished {i+1} wells')




