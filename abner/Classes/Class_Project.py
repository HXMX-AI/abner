import              pandas                       as             pd
from                pathlib                     import          Path
from                Utilities.FilesInDir        import          FilesInDir
import              pickle
import              os, time, datetime



#==================================================================================================
class Project:

    __slots__ = ['dir_prj', 'name', 'dateTime_prj','dateTime_config','dict_config','df_scheduler','depthUnit','df_wellInfo']

    def __init__(self, dir_prj, prj_name, dict_config, file_exts):
        self.name         = prj_name
        self.dir_prj      = dir_prj
        self.dateTime_prj = datetime.datetime.now()
        self.depthUnit    = None
        self.df_wellInfo  = None
        self.df_scheduler = None

        # Load the config file
        path_fName_config    = dir_prj /  "config_logRcnd.xlsx"
        self.dict_config     = pd.read_excel(path_fName_config, sheet_name = None, index_col = 0)
        self.dateTime_config = os.path.getmtime(path_fName_config)



    def Save2Pck(self):
        pckName_out   = self.dir_prj / 'PRJ.pck'
        with open(pckName_out, 'wb') as file:
            pickle.dump(self, file)

        return None


#==================================================================================================
if __name__ == "__main__":

    dir_PROJECTS = Path("C:/Users/ridva/OneDrive/Documents/WELLS")
    project_name = "Csv_Test"
    file_exts    = ['csv','LAS']

    dir_prj           = dir_PROJECTS / project_name
    path_fName_config = dir_prj /  "config_logRcnd.xlsx"
    dict_config       = pd.read_excel(path_fName_config, sheet_name = None, index_col = 0)



    Prj     = Project(dir_prj, project_name, dict_config, file_exts)
    if True :  Prj.Save2Pck()

    print('done')