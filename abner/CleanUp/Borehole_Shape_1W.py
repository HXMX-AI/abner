import  pandas                          as          pd
import  pickle
import  numpy                           as          np
from    Classes.Class_LogDataSet        import      LogDataSet
from    Classes.Class_FileName          import      FileName
from    Utilities.FilesInDir            import      FilesInDir
from    Utilities.Functions_Units       import      Get_Dict_Conv
import  matplotlib.pyplot               as          plt
from    pathlib                         import      Path
from    Utilities.Functions_Units       import      Convert_x
from    Utilities.Say_It                import      Say_It
from    CleanUp.Borehole_Computations   import      Compute_DCAL, Compute_Pseu_DCAL, Compute_Mud_Signal



#===================================================
def Borehole_Shape_1W(PRJ, p_path,  pars_input, dso):

    print(f'Borehole_Shape  in   well: {dso.wellName}')

    dso.moduleName = Path(__file__).stem
    dso.pars_input = pars_input.copy()
    if pars_input['saveDebug']:
        dso.Save2Pck_Debug(str(p_path))

    # CALI, BS Checks
    has_cali = True if 'CALI' in dso.df_varUnitInfo['var_out'] else False
    has_bs   = True if 'BS' in dso.df_varUnitInfo['var_out']   else False

    if not has_cali:                                # NOTHING TO DO
        print('No Caliper, skipping module')
        return PRJ, dso
    elif has_bs:                                    # has CALI, BS, compute DCAL
        dso = Compute_DCAL(PRJ, dso)
    else:                                           # has CALI, but no BS, compute BS_PSEU, then DCAL_PSEU, ...
        print('Will Compute pseudo DCAL')
        dso = Compute_Pseu_DCAL(PRJ, dso)

    # MUD Signal, as long as there is BS            # If has CALI, compute mud signal
    dso = Compute_Mud_Signal(PRJ, dso)




    # HISTORY
    dso.UpdateHistory()

    # SAVE
    if pars_input['save2pck'] :
        dso.Save2Pck(p_path)


    return PRJ, dso





