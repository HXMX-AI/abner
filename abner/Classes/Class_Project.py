import pandas as pd
from pathlib import Path
import pickle
import os, datetime
from typing import Optional


class Project:
    def __init__(self, dir_prj, prj_name):
        self.name: str = prj_name
        self.dir_prj: Path = dir_prj
        self.dateTime_prj: datetime.datetime = datetime.datetime.now()
        self.depthUnit: Optional[str] = None
        self.df_wellInfo: Optional[pd.DataFrame] = None
        self.df_scheduler: Optional[pd.DataFrame] = None

        # Load the config file
        path_fName_config = dir_prj / "config_logRcnd.xlsx"
        self.dict_config = pd.read_excel(
            path_fName_config, sheet_name=None, index_col=0
        )
        self.dateTime_config = os.path.getmtime(path_fName_config)

    def Save2Pck(self):
        pckName_out = self.dir_prj / "PRJ.pck"
        with open(pckName_out, "wb") as file:
            pickle.dump(self, file)

        return None


if __name__ == "__main__":
    dir_PROJECTS = Path("C:/Users/ridva/OneDrive/Documents/WELLS")
    project_name = "Csv_Test"
    file_exts = ["csv", "LAS"]

    dir_prj = dir_PROJECTS / project_name
    path_fName_config = dir_prj / "config_logRcnd.xlsx"
    dict_config = pd.read_excel(path_fName_config, sheet_name=None, index_col=0)

    Prj = Project(dir_prj, project_name)
    if True:
        Prj.Save2Pck()

    print("done")
