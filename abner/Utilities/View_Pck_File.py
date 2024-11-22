import pickle
from pathlib import Path

from abner.GUIs.GUI_GetFileName import GUI_GetFileName


def View_Pck_File(fPath):

    if fPath is None:
        pckFileName = GUI_GetFileName(filetype="pck")
    else:
        pckFileName = Path(fPath)

    with open(pckFileName, "rb") as file:
        dso = pickle.load(file)

    print(f"\n{dso.wellName=}")
    print(dso.df.head(10))
    print(dso.df.tail(10))
    print("\n df_varUnitInfo")
    print(dso.df_varUnitInfo)
    print("\n dict_depthInfo")
    print(dso.dict_depthInfo)
    print("\n HISTORY:")
    print(dso.history)

    return dso


if __name__ == "__main__":
    dso = View_Pck_File(None)
