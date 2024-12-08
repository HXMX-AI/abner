from pathlib import Path
import json
from abner.Utilities.Say_It import Say_It


# =====================================================
def Save_Last_LogView_Run(p_data, p_tmpl):

    if p_data.is_file():
        print("\n", str(p_data), "exists")
    if p_tmpl.is_file():
        print(str(p_tmpl), "exists")

    data_parents = list(p_data.parents)
    tmpl_parents = list(p_tmpl.parents)
    num_min = min(len(data_parents), len(tmpl_parents))
    if len(data_parents) > len(tmpl_parents):
        data_parents, tmpl_parents = tmpl_parents, data_parents
    data_parents.reverse()
    tmpl_parents.reverse()

    p_prj_dir = None
    for i in range(num_min):
        if str(data_parents[i]) == str(tmpl_parents[i]):
            p_prj_dir = data_parents[i]

    if p_prj_dir is not None:
        d_last_run = {
            "prj_dir": str(p_prj_dir),
            "fileName_data": str(p_data),
            "fileName_tmpl": str(p_tmpl),
        }

        fileName = p_prj_dir / "Visuals" / "Last_LogView_Run.json"
        with open(fileName, "w") as json_file:
            json.dump(d_last_run, json_file, indent=4)
    else:
        d_last_run = {}

    return d_last_run


# =====================================================
def Load_Last_LogView_Run(dir_prj):

    fileName = Path(dir_prj) / "Visuals" / "Last_LogView_Run.json"

    if Path(fileName).exists():
        with open(fileName, "r") as json_file:
            d_last_run = json.load(json_file)
    else:
        Say_It("There is no record for a last run")
        d_last_run = {}

    return d_last_run


# ====================================================================================================
if __name__ == "__main__":

    if False:
        p_data = Path(
            "C:\\Users\\ridva\\OneDrive\\Documents\\WELLS\\Groningen\\Debug\\Remove_LinSeg_1W\\fuck.pck"
        )
        p_tmpl = Path(
            "C:\\Users\\ridva\\OneDrive\\Documents\\WELLS\\Groningen\\Visuals\\LogView_zart.xlsx"
        )

    if False:
        p_tmpl = Path(
            "C:\\Users\\ridva\\OneDrive\\Documents\\WELLS\\Groningen\\Debug\\Remove_LinSeg_1W\\fuck.pck"
        )
        p_data = Path(
            "C:\\Users\\ridva\\OneDrive\\Documents\\WELLS\\Groningen\\Visuals\\LogView_zart.xlsx"
        )

    p_data = Path(
        "C:/Users/ridva/OneDrive/Documents/WELLS/ND_152N_101W_20241004_LAS_V2/33053026330000-AIG.pck"
    )
    p_tmpl = Path(
        "C:/Users/ridva/OneDrive/Documents/WELLS/ND_152N_101W_20241004_LAS_V2/Visuals/Log_Template_Separate_Resistivity.xlsx"
    )
    d_last_run = Save_Last_LogView_Run(p_data, p_tmpl)

    print(d_last_run)
