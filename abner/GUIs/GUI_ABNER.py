
import  tkinter                      as              tk
from    tkinter                     import          Menu, Toplevel
from    GUIs.GUI_LogView_COPY       import          Display_Logs
from    PIL                         import          Image, ImageTk
from    GUIs.GUI_Visualization      import          GUI_Visualization



#==========================================================
# Create the main window
root = tk.Tk()
root.title("ABNER")
root.geometry("500x200")

# Load the icon image
icon_project = tk.PhotoImage(file="Project_Tools.png")
original_image = Image.open("Project_Tools.png")
resized_image  = original_image.resize((125,125))
tk_image       = ImageTk.PhotoImage(resized_image)

# Load the icon image
icon_project = tk.PhotoImage(file="Anomaly_Detection.png")
original_image = Image.open("Anomaly_Detection.png")
resized_image_2  = original_image.resize((125,125))
tk_image_2     = ImageTk.PhotoImage(resized_image_2)

# Load the icon image
icon_project = tk.PhotoImage(file="Visualization.png")
original_image = Image.open("Visualization.png")
resized_image_3  = original_image.resize((125,125))
tk_image_3     = ImageTk.PhotoImage(resized_image_3)


#===============================================
def LogView():
    print('ZAAAAAART')
    Display_Logs()

def Gui_Visualization():
    GUI_Visualization()




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
button1 = tk.Button(root, text="Project Tools", image = tk_image, width = 150, height = 150, relief = tk.FLAT)
button2 = tk.Button(root, text="DATA CLEAN UP", image = tk_image_2, width = 150, height = 150, relief = tk.FLAT)
button3 = tk.Button(root, text="DATA CLEAN UP", image = tk_image_3, width = 150, height = 150, relief = tk.FLAT, command= Gui_Visualization)


button1.pack(side = tk.LEFT, padx = 10)
button2.pack(side = tk.LEFT, padx = 10)
button3.pack(side = tk.LEFT, padx = 10)

# Start the main event loop
root.mainloop()