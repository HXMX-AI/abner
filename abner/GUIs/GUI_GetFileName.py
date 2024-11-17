from tkinter import *
from tkinter.filedialog import askopenfilename



# ------------------------------------------------------------------------------
def GUI_GetFileName(filetype='csv'):
    if filetype == 'xlsx':
        list_fileTypes = [('xlsx files', '*.xlsx')]
    elif filetype == 'csv':
        list_fileTypes = [('csv files', '*.csv')]
    elif filetype == 'pck':
        list_fileTypes = [('pck files', '*.pck')]
    elif filetype == 'LAS':
        list_fileTypes = [('pck files', '*.LAS')]
    elif filetype == 'las':
        list_fileTypes = [('pck files', '*.las')]
    elif (filetype == 'all') or (filetype == ''):
        list_fileTypes = [('All files', '*.*')]

    # BeepIt(2000, 50, 1)
    root = Tk()
    root.withdraw()
    full_fname = askopenfilename(title='SELECT A FILE', filetypes=list_fileTypes)
    root.destroy()

    return full_fname


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    full_fname = GetFileName('all')
    print(full_fname)