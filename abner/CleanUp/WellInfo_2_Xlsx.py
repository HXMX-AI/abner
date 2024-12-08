from pathlib import Path


def WellInfo_2_Xlsx(PRJ):

    p_out = Path(PRJ.dir_prj) / "WellInfo.xlsx"
    PRJ.df_wellInfo.to_excel(p_out, index=True)
