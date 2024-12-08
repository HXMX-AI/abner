import  pandas                      as          pd
import  pickle
from   abner. Classes.Class_FileName      import      FileName
from    abner.Utilities.FilesInDir        import      FilesInDir

#=======================================================================================================================
def Remove_Nulls_1W(PRJ, p_path, pars_input, dso):

    dso.moduleName = FileName(__file__).justName
    dso.pars_input = pars_input.copy()
    if pars_input['saveDebug']:
        dso.Save2Pck_Debug(str(p_path))



    df_misc     = PRJ.dict_config['Misc']
    input_row   = df_misc.loc['null_values',:]
    null_values = [s for s in input_row if s == s]
    remove_nulls = df_misc.loc['remove_nulls'].iloc[0]

    if (dso.format_in == 'LAS') and (dso.nullValue is not None):
        nullValue    = dso.nullValue
        cond         = dso.df[:] == nullValue
        if remove_nulls == True:
            dso.df[cond] = None
    elif dso.nullValue is None:
        null_values_found = []

        for null in null_values:                    # for floats/integers
            cond = dso.df[:] == null
            if cond.any().any():
                null_values_found.append(null)
                if remove_nulls == True:
                    dso.df[cond] = None

        for null in null_values:                    # for strings
            cond = dso.df[:] == str(null)
            if cond.any().any():
                print(f'Found null value: {null}')
                null_values_found.append(null)
                if remove_nulls == True:
                    dso.df[cond] = None


        if len(null_values_found) > 1:
            print(f'\t{null_values_found=}')

        #Update null values for dso
        dso.nullValue = null_values_found.copy()

    # HISTORY
    dso.UpdateHistory()

    if pars_input['save2pck'] :
        dso.Save2Pck(p_path)


    if remove_nulls:
        print(f'Removed nulls in  well: {p_path}')
    else:
        print(f'Checked for  nulls in  well: {p_path}')

    return PRJ, dso



#=========================================================================================
if __name__ == '__main__':

    # CONFIG stuff
    dir_config   = "C:/Users/ridva/OneDrive/Documents/WELLS/"
    fName_config = "config_logRcnd.xlsx"
    df_null      = pd.read_excel(dir_config + fName_config, sheet_name ='Nulls')


    # INPUT pck files
    dir_prj      = "C:/Users/ridva/OneDrive/Documents/WELLS/Volve/"
    fileNames    = FilesInDir(dir_prj)

    for pckFileName in fileNames:
        with open(pckFileName, 'rb') as file:
            dso = pickle.load(file)

        # pars_input
        pars_input                 = {}
        pars_input['pckFileName']  = pckFileName
        pars_input['nullList']     = df_null
        pars_input['save2pck']     = True
        pars_input['saveDebug']    = False
        new_dso                    = Remove_Nulls_1W(pars_input, dso)


    print('done')