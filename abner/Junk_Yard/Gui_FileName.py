# importing tkinter and tkinter.ttk
# and all their functions and classes
from tkinter import *
from tkinter.ttk import *

# importing askopenfile function from class filedialog
from tkinter.filedialog import askopenfile

#==================================================================================
def GetFileName(filetype, message):
    root = Tk()
    root.geometry('350x100')

    def open_file():
        fileName = askopenfile(mode='r', filetypes=[('DatasetObj', '*'+filetype)])
        if 1: print(fileName.name)


    btn = Button(root, text= message, command=lambda: open_file())
    btn.pack(side=TOP, pady=10)

    mainloop()

    return fileName.name


#===================================================================================
if __name__ == '__main__':

    filetype = 'pck'
    message  = 'SELECT Dataset File'
    zart     =  GetFileName(filetype, message)
    print(f'{zart=}')