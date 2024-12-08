import tkinter as tk
from tkinter import Menu, Toplevel
from pathlib import Path
import pandas as pd
from abner.GUIs.GUI_Create_New_Project import GUI_Create_New_Project
from abner.GUIs.GUI_Project_Summary import GUI_Project_Summary
from PIL import Image, ImageTk
from abner.config import abner_dir


def GUI_Project_Tools():

    def Create_New_Project():
        GUI_Create_New_Project()
        pass

    def Project_Summary():
        GUI_Project_Summary()
        pass

    root_new = tk.Toplevel()  #  Tk()
    root_new.title("PROJECT TOOLS")
    root_new.geometry("350x200")

    button_font = ("Arial", 10, "bold")

    # Load the icon image
    project_tools_path = abner_dir / "GUIs" / "Project_Tools.png"
    icon_project = tk.PhotoImage(file=str(project_tools_path))
    original_image = Image.open(str(project_tools_path))
    resized_image_3 = original_image.resize((125, 125))
    tk_image_3 = ImageTk.PhotoImage(resized_image_3)

    # # Create a menu bar
    # menu_bar = Menu(root_new)
    # #
    #
    # #Create an edit menu and add it to the menu bar
    # exit_menu = Menu(menu_bar, tearoff=0)
    # exit_menu.add_command(label="Exit", command=root_new.destroy)
    # menu_bar.add_cascade(label="Exit", menu=exit_menu)
    # #
    # # Display the menu bar
    # root_new.config(menu=menu_bar)

    # # Create buttons and place them on the window
    image_label = tk.Label(
        root_new, image=tk_image_3, anchor="e", width=120, height=120
    )
    button1 = tk.Button(
        root_new,
        text="Create New Project",
        anchor="w",
        width=20,
        height=2,
        font=button_font,
        relief=tk.RAISED,
        command=Create_New_Project,
    )
    button2 = tk.Button(
        root_new,
        text="Project Summary",
        anchor="w",
        width=20,
        height=2,
        font=button_font,
        relief=tk.RAISED,
        command=Project_Summary,
    )

    # GRIDDING
    image_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
    button1.grid(row=0, column=1, padx=10, pady=10)
    button2.grid(row=1, column=1, padx=10, pady=10)

    # Start the main event loop
    root_new.mainloop()


# ====================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("TEST")
    root.geometry("10x20")
    GUI_Project_Tools()
