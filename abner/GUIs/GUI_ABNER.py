
import  tkinter                      as              tk
from    tkinter                     import          Menu
from    abner.GUIs.GUI_LogView_COPY       import          Display_Logs
from    PIL                         import          Image, ImageTk
from    abner.GUIs.GUI_Visualization      import          GUI_Visualization
from    abner.GUIs.GUI_Project_Tools      import          GUI_Project_Tools
from    abner.config                        import          abner_dir


#==========================================================
# Create the main window
root = tk.Tk()
root.title("ABNER")
root.geometry("500x200")

# Load the icon image
project_tools_path = abner_dir / "GUIs" / "Project_Tools.png"
icon_project = tk.PhotoImage(file=str(project_tools_path))
original_image = Image.open(str(project_tools_path))
resized_image  = original_image.resize((125,125))
tk_image       = ImageTk.PhotoImage(resized_image)

# Load the icon image
anomaly_detection_path = abner_dir / "GUIs" / "Anomaly_Detection.png"
icon_project = tk.PhotoImage(file=str(anomaly_detection_path))
original_image = Image.open(str(anomaly_detection_path))
resized_image_2  = original_image.resize((125,125))
tk_image_2     = ImageTk.PhotoImage(resized_image_2)

# Load the icon image
visualization_path = abner_dir / "GUIs" / "Visualization.png"
icon_project = tk.PhotoImage(file=str(visualization_path))
original_image = Image.open(str(visualization_path))
resized_image_3  = original_image.resize((125,125))
tk_image_3     = ImageTk.PhotoImage(resized_image_3)


#===============================================
def LogView():
    print('ZAAAAAART')
    Display_Logs()

def Gui_Visualization():
    GUI_Visualization()

def Gui_Project_Tools():
    GUI_Project_Tools()




# Create a menu bar
menu_bar = Menu(root)

# Create a file menu and add it to the menu bar
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")

menu_bar.add_cascade(label="File", menu=file_menu)

# Create Visualization menu
vis_menu = Menu(menu_bar, tearoff=0)
vis_menu.add_command(label="View Logs", command = LogView)
# edit_menu.add_command(label="Copy")
# edit_menu.add_command(label="Paste")
menu_bar.add_cascade(label="Visualization", menu=vis_menu)

# Create an edit menu and add it to the menu bar
exit_menu = Menu(menu_bar, tearoff=0)
exit_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="Exit", menu=exit_menu)

# Display the menu bar
root.config(menu=menu_bar)

# Create buttons and place them on the window
button1 = tk.Button(root, text="Project Tools", image = tk_image, width = 150, height = 150, relief = tk.FLAT, command = Gui_Project_Tools)
button2 = tk.Button(root, text="DATA CLEAN UP", image = tk_image_2, width = 150, height = 150, relief = tk.FLAT)
button3 = tk.Button(root, text="DATA CLEAN UP", image = tk_image_3, width = 150, height = 150, relief = tk.FLAT, command= Gui_Visualization)


button1.pack(side = tk.LEFT, padx = 10)
button2.pack(side = tk.LEFT, padx = 10)
button3.pack(side = tk.LEFT, padx = 10)

# Start the main event loop
root.mainloop()