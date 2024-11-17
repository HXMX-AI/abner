"""
    This module creates LogDataSet objects from all *.csv and *.LAS files found in subfolder Input_Data
    Once the objects are created, they are saved in the project and Input_Data folders (both)

    This module updates PRJ.df_wellInfo with proper well names
"""

from        Utilities.FilesInDir            import          FilesInDir
from        CSV_to_LogDataSet_1W            import          CSV_to_LogDataSet_1W
from        LAS_to_LogDataSet_1W            import          LAS_to_LogDataSet_1W
from        Utilities.Say_It                import          Say_It
import      pandas                          as              pd



#==================================================================================================================
def Input_Files_to_LogDso(PRJ, pars_input):

    # CONVERT ALL FILES - even if pck exist .........................................................
    files_csv  = FilesInDir(PRJ.dir_prj / "Input_Data", extensions = 'csv')
    files_las  = FilesInDir(PRJ.dir_prj / "Input_Data", extensions = 'las')   # 'LAS')

    wellNames_csv   = [f.stem for f in files_csv]
    wellNames_las   = [f.stem for f in files_las]
    wellNames_inter = set(wellNames_csv).intersection(set(wellNames_las))
    assert len(wellNames_inter) == 0, Say_It('WARNING: you have duplicate wells in csv and LAS')

    wellNames   = []
    fileNames   = []
    orgAPIs     = []
    APIs        = []
    UWIs        = []
    orgSampRate = []
    sampRate    = []
    depthUnit   = []

    for path_file in files_csv:
        dso = CSV_to_LogDataSet_1W(PRJ, path_file, pars_input)
        wellNames.append(dso.wellName)
        fileNames.append(dso.fileName)
        orgAPIs.append(dso.orgAPI)
        APIs.append(dso.API)
        UWIs.append(dso.UWI)
        orgSampRate.append(dso.dict_depthInfo['orgSampRate'])
        sampRate.append(dso.dict_depthInfo['sampRate'])
        depthUnit.append(dso.dict_depthInfo['depthUnit'])

    for path_file in files_las:
        dso = LAS_to_LogDataSet_1W(PRJ, path_file, pars_input)
        wellNames.append(dso.wellName)
        fileNames.append(dso.fileName)
        orgAPIs.append(dso.orgAPI)
        APIs.append(dso.API)
        UWIs.append(dso.UWI)
        orgSampRate.append(dso.dict_depthInfo['orgSampRate'])
        sampRate.append(dso.dict_depthInfo['sampRate'])
        depthUnit.append(dso.dict_depthInfo['depthUnit'])

    the_suf                       = 'log.pck'
    all_pck                       = FilesInDir(PRJ.dir_prj / "Input_Data", the_suf)
    df_wellInfo                   = pd.DataFrame(columns=['wellNo', 'keep','wellName','orgAPI','API','UWI','path_pck','orgSampRate','sampRate','xCoord','yCoord', 'nullDepth'], index = wellNames)
    df_wellInfo['wellName']       = wellNames
    df_wellInfo['fileName']       = fileNames
    df_wellInfo['orgAPI']         = orgAPIs
    df_wellInfo['API']            = APIs
    df_wellInfo['UWI']            = UWIs
    df_wellInfo['orgSampRate']    = orgSampRate
    df_wellInfo['sampRate']       = sampRate
    df_wellInfo['depthUnit']      = depthUnit
    df_wellInfo['wellNo']         = range(len(all_pck))
    df_wellInfo['keep']           = 1
    df_wellInfo.loc[:,'path_pck'] = [s.name for s in all_pck]
    df_wellInfo.sort_index(inplace=True)

    # wellName CHECK: are they unique?
    unique_wellNames = list(set(wellNames))
    if len(unique_wellNames) != len(wellNames):
        Say_It(f'\nWARNING: WELL NAMES ARE NOT UNIQUE')
        nameCount = [wellNames.count(s) for s in unique_wellNames]
        [print(f'wellName {unique_wellNames[n]} is repeated {nameCount[n]} times') for n in range(len(unique_wellNames)) if nameCount[n] > 1]


    # fileName CHECK: are they unique?
    unique_fileNames = list(set(fileNames))
    if len(unique_fileNames) != len(fileNames):
        Say_It(f'\nWARNING: FILE NAMES ARE NOT UNIQUE')
        nameCount = [fileNames.count(s) for s in unique_fileNames]
        [print(f'fileName {unique_fileNames[n]} is repeated {nameCount[n]} times') for n in range(len(unique_fileNames)) if nameCount[n] > 1]



    PRJ.df_wellInfo = df_wellInfo

    PRJ.Save2Pck()

    return PRJ