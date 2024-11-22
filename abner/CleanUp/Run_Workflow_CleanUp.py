from pathlib import Path
import pandas as pd
from time import process_time

from abner.CleanUp.Initialize_PRJ import Initialize_PRJ
from abner.Utilities.Functions_Pickle_Files import Read_Pickle_File


def Run_Workflow_CleanUp(dir_prj):
    t1_start = process_time()

    liveData = True
    allDso = {}
    spacer = "." * 80
    df_scheduler = pd.read_excel(dir_prj / "Scheduler.xlsx", index_col="order")

    # INITIALIZE PRJ : MUST BE RUN ..............................................
    print(f"\n{spacer}")
    PRJ = Initialize_PRJ(dir_prj)

    if PRJ == "Not finished":
        return "Run_Workflow_CleanUp NOT FINISHED"

    PRJ.df_scheduler = df_scheduler

    # RUN the PROCESSES
    keys_ = df_scheduler.columns[2:]
    for idx in df_scheduler.index:
        processName = df_scheduler.loc[idx, "processName"]
        run_it = df_scheduler.loc[idx, "run"]
        spacer = "." * (80 - len(str(processName)))

        if run_it:
            print(f"\n{processName}{spacer}")
            if processName == "Input_Files_to_LogDso":
                PRJ = eval(
                    str(df_scheduler.loc[idx, "processName"]) + "(PRJ, pars_input)"
                )
            else:
                path_pck_files = PRJ.df_wellInfo["path_pck"]
                for p in path_pck_files:
                    p_path = PRJ.dir_prj / p
                    dso = Read_Pickle_File(p_path)
                    PRJ, dso = eval(
                        str(df_scheduler.loc[idx, "processName"])
                        + "_1W(PRJ, p_path, pars_input, dso)"
                    )
                    if liveData:
                        allDso[p_path.stem] = dso

    # SAVE THE UPDATED PROJECT
    PRJ.Save2Pck()
    t1_stop = process_time()
    print(f"Clean_Up elapsed time: {t1_stop - t1_start}\n\n")

    return "Run_Workflow_CleanUp FINISHED"


if __name__ == "__main__":

    if True:
        project_name = (
            "JUNK_Nov14_test"  # "ND_152N_101W_20241004_LAS_MP"  "Single_Check"
        )
        dir_WELLS = Path("C:/Users/ridva/OneDrive/Documents/WELLS")
        dir_prj = dir_WELLS / project_name

        status = Run_Workflow_CleanUp(dir_prj)

        print(f"\n completed {dir_prj}: ALL DONE")
