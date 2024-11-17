import  tkinter                 as      tk
from    tkinter                 import  Listbox, Scrollbar, filedialog
from    GUIs.GUI_GetFileName    import  GUI_GetFileName
import  pickle



#=======================================================================================================================
def on_select1(event):
    # Get the selected item(s) from the listbox
    selected_items = listbox1.curselection()
    for index in selected_items:
        print(f"Selected item: {listbox1.get(index)}")

def on_select2(event):
    # Get the selected item(s) from the listbox
    selected_items = listbox2.curselection()
    for index in selected_items:
        print(f"Selected item: {listbox2.get(index)}")

def Select_Project():
    print('Selected project')
    path_prj = filedialog.askdirectory(title="Select a Project")
    project_selected.set(path_prj)


def Select_Well():
    print('Now going to select the well:')
    well_selected.set(GUI_GetFileName('pck') )


def Select_Template():
    print('Now going to select the well:')
    template_selected.set(GUI_GetFileName('xlsx') )

def Display_Selected_Well():
    pass
    # templated_selected = template_selected.get()
    #
    # df_template        = pd.read_excel(template_selected, sheet_name='Template')
    # df_defaults        = pd.read_excel(template_selected, sheet_name='Defaults')
    # gen_defaults       = pd.Series(df_defaults.Value)
    # gen_defaults.index = df_defaults.Property
    # fNameObj           = FileName(templateFile)
    #
    # with open(wd + fName, 'rb') as file:
    #     LogDs = pickle.load(file)
    # df_in = LogDs.df
    #
    # inputs      = {
    #     'fName':        fName,
    #     'df_in':        df_in,
    #     'templateName': fNameObj.justName,
    #     'template':     df_template,
    #     'gen_defaults': gen_defaults
    # }
    #
    # LayoutObj = Make_LogPlot(inputs)

# CREATE MAIN WINDOW ===================================================================================================
root = tk.Tk()
root.title("LOG PLOT (.pck files ONLY)")
root.geometry("800x450")




# MENU BAR =============================================================================================================
menubar = tk.Menu(root)

# SELECT menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Project",  command = Select_Project)
file_menu.add_command(label="Well",     command = Select_Well)
file_menu.add_command(label="Template", command = Select_Template)
menubar.add_cascade(label="Select", menu=file_menu)     # Add the File menu to the menu bar

# EDIT menu
edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Edit Template", command=lambda: print("Edit_Template"))
menubar.add_cascade(label="Edit", menu=edit_menu)

# SAVE menu
save_menu = tk.Menu(menubar, tearoff=0)
save_menu.add_command(label="Save Template", command=lambda: print("Save_Template"))
save_menu.add_command(label="Save Log Display", command=lambda: print("Save_log_display"))
menubar.add_cascade(label="Save", menu=save_menu)

# RUN menu
run_menu = tk.Menu(menubar, tearoff=0)
run_menu.add_command(label="Display Selected Well", command = Display_Selected_Well())
run_menu.add_command(label="Display ALL wells in project", command=lambda: print("Display_ALL_well_project"))
menubar.add_cascade(label="RUN", menu=run_menu)

# EXIT menu
exit_menu = tk.Menu(menubar, tearoff=0)
exit_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Exit", menu=exit_menu)


root.config(menu=menubar)


# WIDGETS======================================================================================================================
# LABELS ............................................................
label_text = ['PROJECT', 'Well', 'Template']
label_idx  = [None] * len(label_text)
for n in range(len(label_text)):
    temp         = tk.Label(root, text = label_text[n])
    label_idx[n] = temp
    temp.grid(row = n+1, column = 0, sticky = tk.W, padx=5)


# ENTRIES ...........................................................
entry_idx = [None, None, None]
for n in [0,2]:
    entry_idx[n] = tk.Entry(root, width = 110)
    entry_idx[n].grid(row = n+1, column = 1, sticky = tk.NSEW, pady=5)


project_selected   = tk.StringVar()
entry_project_selected = tk.Entry(root, width = 110, textvariable = project_selected)
entry_project_selected.grid(row = 1, column = 1, sticky = tk.NSEW, pady=5)
project_selected.set('ZART')

well_selected   = tk.StringVar()
entry_well_selected = tk.Entry(root, width = 110, textvariable = well_selected)
entry_well_selected.grid(row = 2, column = 1, sticky = tk.NSEW, pady=5)


template_selected   = tk.StringVar()
entry_template_selected = tk.Entry(root, width = 110, textvariable = template_selected)
entry_template_selected.grid(row = 3, column = 1, sticky = tk.NSEW, pady=5)
template_selected.set('Who kinows')






# FRAME 2 ==============================================================================================================
frame2     = tk.Frame(root, width = 300, height= 300, bg= 'lightgray', relief=tk.RAISED)
frame2.grid(row=5, column = 1, columnspan = 1, padx = 10, pady = 30, sticky = tk.E)

label_temp = tk.Label(frame2, text = 'TEMPLATES in Project')
label_temp.pack(side= tk.TOP, fill= tk.BOTH)

#  Create a scrollbar
scrollbar2 = tk.Scrollbar(frame2, orient=tk.VERTICAL, width=20)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox and attach the scrollbar
listbox2= tk.Listbox(frame2, yscrollcommand=scrollbar2.set, width = 50, height = 18)
listbox2.pack(side=tk.LEFT, fill=tk.BOTH)

# Configure the scrollbar
scrollbar2.config(command=listbox2.yview)

for i in range(100, 125):
    listbox2.insert("end", f"Item {i}")




listbox1.bind("<<ListboxSelect>>", on_select1)
listbox2.bind("<<ListboxSelect>>", on_select2)








root.mainloop()
