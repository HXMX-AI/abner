"""
    Pre-requisite:  A prj.pck file must exist for the initialization to take place.
                    The PRJ.pck file is created by the Create_New_Project module.

    This module ensures the dict_config in PRJ.pck is the same as what is in config_logRcnd.xlsx
    If there is a user change made to config_logRcnd.xlsx, this module will update
    dict_config in PRJ.pck with the most recent version of dict_config derived from config_logRcnd.xlsx. 
"""


from        abner.Utilities.FilesInDir            import          FilesInDir
import      pickle
import      os, datetime
import      pandas                          as              pd
from        abner.Utilities.Say_It                import          Say_It


#=======================================================================================================================
def Initialize_PRJ(dir_prj):
    
    # PRJ.pck exists, has config been updated?
    temp = FilesInDir(dir_prj, extensions='pck')
    if len(temp) == 0:
        Say_It('WARNING: No PRJ.pck found')
        print('Set up a project project to continue')
        return 'Not finished'
    else:
        PRJ_fName = dir_prj / 'PRJ.pck'
        with open(PRJ_fName, "rb") as input_file:
            PRJ = pickle.load(input_file)

        # config file has been updated?
        dateTime_config_now = os.path.getmtime(dir_prj / 'config_logRcnd.xlsx')
        if dateTime_config_now == PRJ.dateTime_config:
            print('PRJ config and current config match')
        else:  # Newer config in teh folder
            print('Updating PRJ config')
            PRJ.dateTime_prj    = datetime.datetime.now()
            PRJ.dateTime_config = dateTime_config_now
            PRJ.dict_config     = pd.read_excel(dir_prj / 'config_logRcnd.xlsx', sheet_name=None, index_col=0)
            #PRJ.UpDateWellInfo()
            PRJ.Save2Pck()

    print('Initialize_Project finished')

    return PRJ