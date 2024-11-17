import  tkinter                                 as              tk
from    pathlib                                 import          Path
import  pandas                                  as              pd
import  pickle
from    Visualization.Make_LogPlot              import          Make_LogPlot
from    GUIs.GUI_GetFileName                    import          GUI_GetFileName
from    Visualization.Last_LogView_Run          import          Save_Last_LogView_Run, Load_Last_LogView_Run
from    Utilities.FilesInDir                    import          FilesInDir
from    Utilities.Say_It                        import          Say_It






#=======================================================================================================================
def Select_Project():
    path_prj = tk.filedialog.askdirectory(title="Select a Project")
    prjName.set(str(path_prj))

    # Last settings for the project
    d_last_run = Load_Last_LogView_Run(path_prj)
    if len(d_last_run) > 0:
        wellName.set(str(d_last_run['fileName_data']))
        template_selected.set(str(d_last_run['fileName_tmpl']))

    # Populate the list box with all the files in the project

    files_in_dir = FilesInDir(path_prj, extensions = ['log.pck','csv'])
    listbox1.delete(0, tk.END)
    for i in range(len(files_in_dir)):
        listbox1.insert("end", f" {files_in_dir[i].name}")

    # Populate the template box with all the templates in the project
    dir_vis      = Path(path_prj)  / 'Visuals'
    files_in_vis = FilesInDir(dir_vis, extensions = 'xlsx')
    if files_in_vis is not None:
        listbox2.delete(0, tk.END)
        for i in range(len(files_in_vis)):
            listbox2.insert(tk.END, f" {files_in_vis[i].name}")
    else:
        Say_It('Ritto, fix this habibi')



def Select_Template():
    template_sel = GUI_GetFileName('xlsx')
    template_selected.set(str(template_sel))



def Select_Well():
    wellName_sel = GUI_GetFileName('all')
    wellName.set(wellName_sel)
    temp  = Path(wellName_sel)
    prjName.set(str(temp.parent))    # MAYBE not set this? But then files and prj may be different



def Display_Selected_Well():
    wellName_     = (wellName.get()).strip()
    if str(Path(wellName_).parent) == '.':
        temp0 = prjName.get()
        temp1 = Path(temp0) / wellName_
        p_path = str(temp1)
    else:
        p_path = wellName_

    template_sel_ = (template_selected.get()).strip()
    if str(Path(template_sel_).parent) == '.':
        temp0 = prjName.get()
        temp1 = Path(temp0) / 'Visuals' / template_sel_
        template_sel = str(temp1)
    else:
        template_sel = template_sel_

    print(f'\nThe wellName is {p_path}, \n{template_sel=}')

    df_template        = pd.read_excel(template_sel, sheet_name='Template')
    df_defaults        = pd.read_excel(template_sel, sheet_name='Defaults')
    gen_defaults       = pd.Series(df_defaults.Value)
    gen_defaults.index = df_defaults.Property


    # Check if it is a log.pck file or a csv.
    if Path(p_path).suffix == '.csv':
        df_in = pd.read_csv(p_path, skiprows=range(1, 2))
        print('Cant do it yet')
    else:
        with open(p_path, 'rb') as file:
            LogDs = pickle.load(file)
        df_in = LogDs.df


    #
    inputs      = {
        'fName':        p_path,
        'df_in':        df_in,
        'templateName': 'TemplateName',
        'template':     df_template,
        'gen_defaults': gen_defaults
    }
    #
    status = Make_LogPlot(inputs)

    # Save the last well and last template
    if status == 'done':
        Save_Last_LogView_Run(Path(p_path), Path(template_sel))


def on_select1(event):
    selected_items = listbox1.curselection()
    try:
        well_selected = listbox1.get(selected_items[0])
        wellName.set(well_selected)
    except:
        pass


def on_select2(event):
    which_templates = listbox2.curselection()
    try:
        which_template  = listbox2.get(which_templates)
        template_selected.set(which_template)
    except:
        pass







# CREATE MAIN WINDOW ===================================================================================================
root = tk.Tk()
root.title("LOG PLOT (log.pck files ONLY)")
root.geometry("800x550")



# LABELS ===============================================================================================================
label_text = ['','Project', 'Well', 'Template']
label_idx  = [None] * len(label_text)
n          = 0
for n in range(len(label_text)):
    temp         = tk.Label(root, text = label_text[n])
    label_idx[n] = temp
    temp.grid(row = n+1, column = 0, sticky = tk.W, padx=5, pady = 5 )


# ENTRIES ==============================================================================================================
# project Name
n=1
prjName   = tk.StringVar()
e_prjName = tk.Entry(root, width = 110, textvariable = prjName)
e_prjName.grid(row = n+1, column = 1, sticky = tk.NSEW, pady=5)

# wellName
wellName   = tk.StringVar()
e_wellName = tk.Entry(root, width = 110, textvariable = wellName)
e_wellName.grid(row = n+2, column = 1, sticky = tk.NSEW, pady=5)


# Template
template_selected   = tk.StringVar()
e_template_selected = tk.Entry(root, width = 110, textvariable = template_selected)
e_template_selected.grid(row = n+3, column = 1, sticky = tk.NSEW, pady=5)


# FRAME 1 ==============================================================================================================
frame1     = tk.Frame(root, width = 300, height= 350,  bg= 'yellow', relief=tk.RAISED)
frame1.grid(row=5, column = 0, columnspan = 2, padx = 40, pady = 20, sticky = tk.W)


# Files list box ................
label_temp = tk.Label(frame1, text = 'WELLS in Project')
label_temp.pack(side= tk.TOP, fill= tk.BOTH)

# Create a scrollbar
scrollbar1 = tk.Scrollbar(frame1, orient=tk.VERTICAL, width=20)
scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox and attach the scrollbar
listbox1= tk.Listbox(frame1, yscrollcommand=scrollbar1.set, width = 50, height = 22)
listbox1.pack(side=tk.LEFT, fill=tk.BOTH)
listbox1.bind('<<ListboxSelect>>', on_select1)



# Frame 2 ==============================================================================================================
frame2     = tk.Frame(root, width = 300, height= 300, bg= 'lightgray', relief=tk.RAISED)
frame2.grid(row=5, column = 1, columnspan = 1, padx = 0, pady = 30, sticky = tk.E)

# Templates list box ................
label_temp = tk.Label(frame2, text = 'Templates in Project')
label_temp.pack(side= tk.TOP, fill= tk.BOTH)

# Create a scrollbar
scrollbar2 = tk.Scrollbar(frame2, orient=tk.VERTICAL, width=20)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox and attach the scrollbar
listbox2= tk.Listbox(frame2, yscrollcommand=scrollbar2.set, width = 50, height = 22)
listbox2.pack(side=tk.RIGHT, fill=tk.BOTH)
listbox2.bind('<<ListboxSelect>>', on_select2)


# Configure the scrollbar
scrollbar1.config(command=listbox1.yview)
scrollbar2.config(command=listbox2.yview)







# MENUS ================================================================================================================
menubar = tk.Menu(root)
root.config(menu=menubar)

# Add a Menu item
select_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Select", menu=select_menu)
select_menu.add_command(label="Select Project", command=Select_Project)
select_menu.add_command(label="Select Well", command=Select_Well)
select_menu.add_command(label="Select Template", command=Select_Template)

# Add a Menu item
display_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Display", menu=display_menu)
display_menu.add_command(label="Display Selected Well", command=Display_Selected_Well)

# EXIT menu
exit_menu = tk.Menu(menubar, tearoff=0)
exit_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Exit", menu=exit_menu)


root.mainloop()