from    abner.Classes.Class_FileName      import  FileName
import  datetime
import  pickle
import  os, os.path
from    abner.Utilities.Say_It    import  Say_It
import  pandas              as      pd



#=======================================================================================================================
class LogDataSet:
    __slots__     = ['p_path','fileName','wellName','format_in','nullValue','datasetName','sampRate','df','misc',
                     'history', 'pars_input', 'moduleName', 'df_varUnitInfo', 'dict_depthInfo','duplVars',
                     'orgAPI','API','UWI','Xcoord','Ycoord','LAT','LON','df_OOR', 'df_linSeg']


    def __init__(self):
        self.p_path         = None
        self.fileName       = None
        self.wellName       = None
        self.format_in      = None
        self.nullValue      = None
        self.datasetName    = None
        self.sampRate       = None          # also a key in dict_depthInfo
        self.df             = None
        self.misc           = None
        self.history        = []
        self.pars_input     = None
        self.moduleName     = None


        # df_varUnitInfo
        self.df_varUnitInfo = pd.DataFrame(columns = ['var_in', 'unit_in','var_out','unit_out','unitValid'], dtype=str)


        # dict_depthInfo
        keyList             = ['depthName','depthName_in','depthUnit','hasReversal','hasGaps','orgSampRate','sampRate','numNulls','Remarks']
        self.dict_depthInfo = {key: None for key in keyList}

        self.duplVars  = None
        self.API       = None
        self.orgAPI    = None
        self.UWI       = None
        self.Xcoord    = None
        self.Ycoord    = None
        self.LAT       = None
        self.LON       = None
        self.df_OOR    = None
        self.df_linSeg = None


    def UpdateHistory(self):
        history_update = [self.moduleName, str(datetime.datetime.now()), self.pars_input]
        self.history.append(history_update)
        return self


    def Save2Pck(self, pckName_out):
        with open(pckName_out, 'wb') as file:
            pickle.dump(self, file)


    def Save2Pck_Debug(self, fName):
        fNameObj         = FileName(fName)

        # dir_debug Check
        dir_debug        = os.path.join(fNameObj.dirName, 'Debug')
        if not os.path.isdir(dir_debug):
            message = 'Directory Debug does not exist, creating it'
            Say_It(message)
            os.mkdir(dir_debug)

        # dir_debug_module check
        dir_debug_module = os.path.join(fNameObj.dirName, 'Debug', self.moduleName)
        if not  os.path.isdir(dir_debug_module):
            message = 'Directory ' +  str(self.moduleName) + ' does not exist, creating it'
            Say_It(message)
            os.mkdir(dir_debug_module)

        pckName_out = os.path.join(dir_debug_module, fNameObj.fileName)
        with open(pckName_out, 'wb') as file:
            pickle.dump(self, file)


    # Keep track of sampling rates
    def Update_SampRate(self, sampRate,*args):
        self.sampRate                   = sampRate
        self.dict_depthInfo['sampRate'] = sampRate
        if len(args) == 1:
            self.dict_depthInfo['orgSampRate'] = args[0]
        return self

    def Add_Variable(self, x, varNew, unitNew):
        self.df[varNew] = x
        self.Update_VarUnitInfo(varNew, unitNew)
        return self

    def Update_VarUnitInfo(self, varNew, unitNew):
        temp_index = list(self.df_varUnitInfo.index)
        numRows    = len(temp_index)
        if varNew not in temp_index:
            df_varUnitInfo = self.df_varUnitInfo.copy()
            df_varUnitInfo.loc[numRows+1] = [varNew, unitNew, varNew, unitNew, True]
            temp_index.append(varNew)
            df_varUnitInfo.index =  temp_index
            self.df_varUnitInfo = df_varUnitInfo
        else:
            pass

        return self


