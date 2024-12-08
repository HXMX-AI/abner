import pandas as pd
from abner.Utilities.FilesInDir       import FilesInDir
from abner.Classes.Class_ImmutableDataFrame  import ImmutableDataFrame

def WellInfo_Create(PRJ, path_file_names):

    column_names = ['wellNo',
                    'keep',
                    'wellName',
                    'path_pck',
                    'orgAPI',
                    'API',
                    'UWI',
                    'depthUnit',
                    'orgSampRate',
                    'sampRate',
                    'nullDepth',
                    'Top',
                    'Bottom',
                    'duplVars']

    df_temp      = pd.DataFrame(columns = column_names, index = path_file_names)
    df_wellInfo  = ImmutableDataFrame(df_temp)

    return df_wellInfo