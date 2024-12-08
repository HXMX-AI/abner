import tkinter as tk
from tkinter import Menu
from pathlib import Path
from abner.Utilities.Find_Folder_From_Anywhere import Find_Folder_From_Anywhere
from abner.CleanUp.Create_New_Project import Create_Prj


def GUI_Create_New_Project():

    def Create_Project():
        temp = wells_directory.get()
        temp.strip()
        dir_PROJECTS = Find_Folder_From_Anywhere(temp)
        # dir_PROJECTS = Path(wells_directory.get())
        project_name = prj_name.get()
        Create_Prj(Path(dir_PROJECTS), project_name)

    def Change_Directory():
        result = Find_Folder_From_Anywhere(wells_directory.get())
        wells_directory.set(result)
        print(f"{result=}")

    root_new = tk.Toplevel()  #  Tk()
    root_new.title("CREATE NEW PROJECT")
    root_new.geometry("400x100")
    button_font = ("Arial", 10, "bold")

    # MENU BAR
    menu_bar = Menu(root_new)

    # Create a file menu and add it to the menu bar
    prj_menu = Menu(menu_bar, tearoff=0)
    prj_menu.add_command(label="Create New Project", command=Create_Project)
    menu_bar.add_cascade(label="Project Management", menu=prj_menu)

    root_new.config(menu=menu_bar)

    # Create the first row with an entry box and a button
    wells_directory = tk.StringVar()
    prj_name = tk.StringVar()

    label1 = tk.Label(root_new, text="Projects Directory", anchor="w", justify="left")
    entry1 = tk.Entry(root_new, width=40, textvariable=wells_directory)
    label2 = tk.Label(root_new, text="Project Name", anchor="w", justify="left")
    entry2 = tk.Entry(root_new, width=40, textvariable=prj_name)
    button1 = tk.Button(root_new, text="Change", command=Change_Directory)
    button2 = tk.Button(root_new, text="CREATE PROJECT", command=Create_Project)

    wells_directory.set("WELLS")
    prj_name.set("")

    label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry1.grid(row=0, column=1, padx=10, pady=10)
    label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry2.grid(row=1, column=1, padx=10, pady=10)
    # button1.grid(row=0, column=1, padx=10, pady=10)
    # button2.grid(row=1, column=1, padx=10, pady=10)

    # Start the main event loop
    root_new.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("TEST")
    root.geometry("10x20")
    GUI_Create_New_Project()
