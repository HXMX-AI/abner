"""
    Variable harmonization MUST be done before unit harmonization because:
        units are harmonized only for the variables defined in the Harmonization table.
        unit conversion is not done for variables that are not in the Harmonization table.
"""

from    Classes.Class_FileName      import      FileName
from    Utilities.Functions_Units   import      Get_Dict_Conv
from    Utilities.Say_It            import      Say_It




#=======================================================================================================================
def Harmonize_Units_1W(PRJ, p_path, pars_input, dso):

    if True: print(f'Checked units in  well: {dso.wellName}')

    dso.moduleName = FileName(__file__).justName
    dso.pars_input = pars_input.copy()
    if pars_input['saveDebug']:
        dso.Save2Pck_Debug(str(p_path))



    df_harm        = PRJ.dict_config['Harmonization']
    df_unitNames   = PRJ.dict_config['UnitsRecog']
    df_unitConvLin = PRJ.dict_config['UnitConvLin']
    df_varUnitInfo = dso.df_varUnitInfo.copy()


    # set_unitNames is the set of ALL 'recognized' unit names
    # if a variable is in set_unitNames, its unitName will change, but no conversion will be needed
    # example g/cm3 gets changed to g/cc, but no numeric conversion is needed
    list_unitNames = sum(df_unitNames.iloc[:,:].astype(str).values.tolist(), [])
    tmp_unitNames  = set(list_unitNames)
    if 'nan' in tmp_unitNames: tmp_unitNames.remove('nan')
    set_unitNames  = set()
    [set_unitNames.add(s.casefold()) for s in tmp_unitNames]


    # Find the variables that are eligible for conversion, i.e., only those that are in the harmonization table
    var_intersection = set(df_varUnitInfo['var_out']).intersection(set(df_harm.index))



    for  var in var_intersection:

        if df_varUnitInfo.loc[var,'unit_out'].casefold() in set_unitNames:              # if an alias exists, just rename using the harmonized unit
            df_varUnitInfo.loc[var,'unitValid'] = True
            # Make sure it is the unit defined in Harmonization table ('inches' must become 'in')
            if var == 'DEPTH':                                              # DEPTH has multiple values, ft or m
                temp_unit =  dso.dict_depthInfo['depthUnit'].lower()
                if temp_unit.lower().startswith('f') :
                    temp_out = 'ft'
                elif temp_unit.lower().startswith('m'):
                    temp_out = 'mt'
                dso.dict_depthInfo['depthUnit']     = temp_out
                df_varUnitInfo.loc[var, 'unit_out'] = temp_out
            else:
                df_varUnitInfo.loc[var,'unit_out'] = df_harm.loc[var,'Unit']
        else:                                                                           # no alias, DO conversion if conversioin is defined
            df_varUnitInfo.loc[var, 'unitValid'] = False
            unit_in     = df_varUnitInfo.loc[var,'unit_in']
            unit_out    = df_harm.loc[var,'Unit']
            dict_conv   = Get_Dict_Conv(df_unitConvLin, unit_in, unit_out)

            if dict_conv != {}:
                dso.df[var] = ( dso.df[var] + dict_conv['bias']) * dict_conv['mult']
                df_varUnitInfo.loc[var,'unit_out']  = unit_out
                df_varUnitInfo.loc[var,'unitValid'] = True
                message = f'\tWell {dso.wellName} log {var} unit {unit_in} changed to {unit_out}'
                print(message)

    # NEUTRON check pu mis-listed as v/v
    if 'NPHI' in dso.df.columns:
        nphi_median = dso.df['NPHI'].median()
        if nphi_median > 1.0:
            Say_It('WARNING NEUTRON')
            print(f'\tfile {p_path} has a Neutron listed in units of  v/v but it is  PU or %')
            print(f'\tAbner is going to convert NPHI to v/v')
            dso.df['NPHI']                          =  dso.df['NPHI'] * 0.01
            df_varUnitInfo.loc['NPHI', 'unit_out']  = 'v/v'
            df_varUnitInfo.loc['NPHI', 'unitValid'] = True

    dso.df_varUnitInfo = df_varUnitInfo.copy()

    # HISTORY
    dso.UpdateHistory()

    # SAVE
    if pars_input['save2pck'] :
        dso.Save2Pck(p_path)




    return PRJ, dso




