import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from abner.Utilities.Find_Folder_From_Anywhere import Find_Folder_From_Anywhere


def GUI_Project_Summary():

    def Create_Summary():
        print("Going to create project summary")

    def Select_Project():
        path_prj = filedialog.askdirectory(title="Select a Project")
        prj_dir.set(str(path_prj))

    root_new = tk.Toplevel()  #  Tk()
    root_new.title("PROJECT SUMMARY")
    root_new.geometry("850x100")
    button_font = ("Arial", 10, "bold")

    # MENU BAR
    menu_bar = tk.Menu(root_new)

    # Create a file menu and add it to the menu bar
    prj_menu = tk.Menu(menu_bar, tearoff=0)
    prj_menu.add_command(label="Create Project Summary", command=Create_Summary)
    menu_bar.add_cascade(label="RUN", menu=prj_menu)

    root_new.config(menu=menu_bar)

    # Create the first row with an entry box and a button
    prj_dir = tk.StringVar()
    summary_type = tk.StringVar()

    label1 = tk.Label(root_new, text="Project Directory", anchor="w", justify="left")
    entry1 = tk.Entry(root_new, width=100, textvariable=prj_dir)
    button1 = tk.Button(root_new, text="SELECT", command=Select_Project)

    label2 = tk.Label(root_new, text="Summary Type", anchor="w", justify="left")
    entry2 = tk.Entry(root_new, width=40, textvariable=summary_type)
    button2 = tk.Button(root_new, text="CREATE PROJECT")

    prj_dir.set("")
    summary_type.set("Standard")

    label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry1.grid(row=0, column=1, padx=10, pady=10)
    button1.grid(row=0, column=2, padx=10, pady=10)
    label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Start the main event loop
    root_new.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("TEST")
    root.geometry("10x20")
    GUI_Project_Summary()
