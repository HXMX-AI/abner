import datetime
import pickle
import os, os.path
import pandas as pd
from typing import Optional

from abner.Utilities.Say_It import Say_It
from abner.Classes.Class_FileName import FileName


class LogDataSet:
    def __init__(self):
        self.fileName: Optional[str] = None
        self.wellName: Optional[str] = None
        self.format_in: Optional[str] = None
        self.nullValue: Optional[str] = None
        self.datasetName: Optional[str] = None
        self.sampRate: Optional[float] = None  # also a key in dict_depthInfo
        self.df: Optional[pd.DataFrame] = None
        self.misc: Optional[dict] = None
        self.history: list = []
        self.pars_input: Optional[dict] = None
        self.moduleName: Optional[str] = None

        # df_varUnitInfo
        self.df_varUnitInfo = pd.DataFrame(
            columns=["var_in", "unit_in", "var_out", "unit_out", "unitValid"], dtype=str
        )

        # dict_depthInfo
        keyList = [
            "depthName",
            "depthName_in",
            "depthUnit",
            "hasReversal",
            "hasGaps",
            "orgSampRate",
            "sampRate",
            "numNulls",
            "Remarks",
        ]
        self.dict_depthInfo = {key: None for key in keyList}

        self.API = None | float
        self.orgAPI = None | float
        self.UWI = None | str
        self.Xcoord = None | float
        self.Ycoord = None | float
        self.LAT = None | float
        self.LON = None | float
        self.df_OOR = None | pd.DataFrame()
        self.df_linSeg = None | pd.DataFrame()

    def UpdateHistory(self):
        history_update = [
            self.moduleName,
            str(datetime.datetime.now()),
            self.pars_input,
        ]
        self.history.append(history_update)
        return self

    def Save2Pck(self, pckName_out):
        with open(pckName_out, "wb") as file:
            pickle.dump(self, file)

    def Save2Pck_Debug(self, fName):
        fNameObj = FileName(fName)

        # dir_debug Check
        dir_debug = os.path.join(fNameObj.dirName, "Debug")
        if not os.path.isdir(dir_debug):
            message = "Directory Debug does not exist, creating it"
            Say_It(message)
            os.mkdir(dir_debug)

        # dir_debug_module check
        dir_debug_module = os.path.join(fNameObj.dirName, "Debug", str(self.moduleName))
        if not os.path.isdir(dir_debug_module):
            message = (
                "Directory " + str(self.moduleName) + " does not exist, creating it"
            )
            Say_It(message)
            os.mkdir(dir_debug_module)

        pckName_out = os.path.join(dir_debug_module, fNameObj.fileName)
        with open(pckName_out, "wb") as file:
            pickle.dump(self, file)

    # Keep track of sampling rates
    def Update_SampRate(self, sampRate, *args):
        self.sampRate = sampRate
        self.dict_depthInfo["sampRate"] = sampRate
        if len(args) == 1:
            self.dict_depthInfo["orgSampRate"] = args[0]
        return self

    def Add_Variable(self, x, varNew, unitNew):
        if self.df is None:
            raise ValueError("DataFrame is not initialized")

        self.df[varNew] = x
        self.Update_VarUnitInfo(varNew, unitNew)
        return self

    def Update_VarUnitInfo(self, varNew, unitNew):
        temp_index = list(self.df_varUnitInfo.index)
        numRows = len(temp_index)
        if varNew not in temp_index:
            df_varUnitInfo = self.df_varUnitInfo.copy()
            df_varUnitInfo.loc[numRows + 1] = [varNew, unitNew, varNew, unitNew, True]
            temp_index.append(varNew)
            df_varUnitInfo.index = pd.Index(temp_index)
            self.df_varUnitInfo = df_varUnitInfo
        else:
            pass

        return self
