import pickle
from pathlib import Path


# =======================================================
def Load_PRJ(dir_prj):

    PRJ_fName = dir_prj / "PRJ.pck"
    with open(PRJ_fName, "rb") as input_file:
        PRJ = pickle.load(input_file)

    return PRJ


# ======================================================
if __name__ == "__main__":

    project_name = "CoreGL_REDO"  # "LINSEG_TEST_2"
    dir_WELLS = Path("C:/Users/ridva/OneDrive/Documents/WELLS")
    dir_prj = dir_WELLS / project_name

    zart = Load_PRJ(dir_prj)

    print("done")
