import pandas           as      pd
from Junk_Yard.Class_FileName_NoStatic import  FileName

class LogTmpl:

    __slots__ = ('name','df_in','tmpl','num_tracks','num_logs','tr_len','logs_per_track','df_coords','tr_xlen','tr_ylen')

    def __init__(self, name, df_in):
        self.name  = name
        self.df_in = df_in
        self.tmpl  = self.df_in.copy()

        self.RemoveNoShows()
        self.SetTracks()

        print('DONT USE THIS, use instead Class_Layout')

    # def RemoveNoShows(self):
    #     # Drop those not bo be displayed
    #     self.tmpl = self.tmpl[self.tmpl['show'] != 0].copy()
    #     return self

    # How many tracks
    def SetTracks(self):
        xMargin = 0.050
        yMargin = 0.025
        headerY = 0.025

        # track_labels      = self.tmpl['trNum'].unique()
        # track_labels.sort()
        # self.num_tracks   = len(track_labels)
        # self.num_logs     = self.tmpl.shape[0]

        # # Sort Tracks and create index
        # self.tmpl.sort_values(by=['trNum'], inplace=True)
        # self.tmpl.index = range(self.tmpl.shape[0])
        #
        # # Track Numbers modified
        # org_to_new = pd.Series(range(self.num_tracks), index=track_labels)
        # for n in range(self.num_logs):
        #     self.tmpl.loc[n, 'trNum'] = org_to_new[self.tmpl.loc[n, 'trNum']]

        # # Track lengths
        # self.tr_len          = [None] * self.num_tracks
        # self.logs_per_track  = [None] * self.num_tracks
        # sum_tr_len           = 0
        # for n in range(self.num_tracks):
        #     cond = self.tmpl.trNum == n
        #     temp                   = self.tmpl.loc[cond,'trLen']
        #     self.tr_len[n]         = temp.max()
        #     self.logs_per_track[n] = len(temp)
        #     sum_tr_len             = sum_tr_len + self.tr_len[n]

        # # Consider xMargin
        # scaler = (1-2*xMargin) / sum_tr_len
        #
        # # xlen for each track
        # self.tr_xlen = [temp * scaler  for temp in self.tr_len].copy()

        # ylen for each track
        # header_rows   = max(self.logs_per_track)
        # header_height = header_rows * headerY
        # self.tr_ylen  = 1.0 - (2*yMargin) - header_height

        # Coordinates for all axes
        # df_coords          = pd.DataFrame(columns = ['xLeft','yBot','xLen','yLen'], index = range(self.num_tracks))
        # df_coords['xLen']  = self.tr_xlen.copy()
        # df_coords['yBot']  = yMargin
        # df_coords['yLen']  = self.tr_ylen

        xRight_last = xMargin
        xL     = [None] * self.num_tracks
        xR     = [None] * self.num_tracks
        for n in range(self.num_tracks):
            xL[n]       =  xRight_last
            xR[n]       =  xL[n]+self.tr_xlen[n]
            xRight_last = xR[n]

        df_coords['xLeft'] = xL.copy()
        self.df_coords     = df_coords


        return self



#======================================================================================================
if __name__ == "__main__":

    templateFile   = "C:/Users/ridva/OneDrive/Documents/WELLS/" + "Log_Template_Volve.xlsx"
    df_in          = pd.read_excel(templateFile)

    fNameObj       = FileName(templateFile)

    tmplObj        = LogTmpl(fNameObj.justName, df_in)

    print(tmplObj.tmpl)