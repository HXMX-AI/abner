from        pathlib                             import          Path
from        CleanUp.Initialize_PRJ              import          Initialize_PRJ
from        CleanUp.Input_Files_to_LogDso       import          Input_Files_to_LogDso
from        CleanUp.Harmonize_Variables_1W      import          Harmonize_Variables_1W
from        CleanUp.Harmonize_Units_1W          import          Harmonize_Units_1W
from        CleanUp.Depth_Check_1W              import          Depth_Check_1W
from        CleanUp.Borehole_Shape_1W           import          Borehole_Shape_1W
from        CleanUp.Remove_Nulls_1W             import          Remove_Nulls_1W
from        CleanUp.Remove_OOR_1W               import          Remove_OOR_1W
from        CleanUp.Remove_LinSeg_1W            import          Remove_LinSeg_1W
from        CleanUp.Trim_Top_Bot_1W             import          Trim_Top_Bot_1W
from        CleanUp.Casing_Check_1W             import          Casing_Check_1W
from        CleanUp.Update_Project_WellInfo_1W  import          Update_Project_WellInfo_1W
from        Utilities.Functions_Pickle_Files    import          Read_Pickle_File
import      pandas                              as              pd
from        Utilities.LogDso_to_csv             import          LogDso_to_csv_1W
from        time                                import          process_time
from        Utilities.Say_It                    import          Say_It
from        shutil                              import          copy




#====================================================================================
def Run_Workflow_CleanUp(dir_prj):
    t1_start = process_time()

    liveData     = True
    allDso       = {}
    spacer       = '.'*80
    df_scheduler = pd.read_excel(dir_prj / "Scheduler.xlsx", index_col = 'order')


    # INITIALIZE PRJ : MUST BE RUN ..............................................
    print(f'\n{spacer}')
    PRJ                      = Initialize_PRJ(dir_prj)
    PRJ.df_scheduler         = df_scheduler



    # RUN the PROCESSES
    keys_          = df_scheduler.columns[2:]
    for idx in df_scheduler.index:
        processName = df_scheduler.loc[idx, 'processName']
        run_it      = df_scheduler.loc[idx,'run']
        values_     = df_scheduler.loc[idx, keys_]
        pars_input  = dict(zip(keys_, values_))
        spacer      = '.' * (80- len(processName))

        if run_it:
            print(f'\n{processName}{spacer}')
            if processName == 'Input_Files_to_LogDso':
                PRJ = eval(df_scheduler.loc[idx, 'processName'] + '(PRJ, pars_input)')
            else:
                path_pck_files = PRJ.df_wellInfo['path_pck']
                for p in path_pck_files:
                    p_path   = PRJ.dir_prj / p
                    dso      = Read_Pickle_File(p_path)
                    PRJ, dso = eval(df_scheduler.loc[idx, 'processName'] + '_1W(PRJ, p_path, pars_input, dso)')
                    if liveData: allDso[p_path.stem] = dso

    # SAVE THE UPDATED PROJECT
    PRJ.Save2Pck()
    t1_stop = process_time()
    print(f'Clean_Up elapsed time: {t1_stop - t1_start}\n\n')

    return 'Run_Workflow_CleanUp FINISHED'


#==================================================================================
if __name__ == '__main__':

    if True:
        project_name = "JUNK_Nov14_test"                  # "ND_152N_101W_20241004_LAS_MP"  "Single_Check"        #
        dir_WELLS    =  Path("C:/Users/ridva/OneDrive/Documents/WELLS")
        dir_prj      =  dir_WELLS / project_name

        status = Run_Workflow_CleanUp(dir_prj)

        print(f'\n completed {dir_prj}: ALL DONE')