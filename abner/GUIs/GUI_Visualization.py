import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk

from abner.GUIs.GUI_LogView_COPY import Display_Logs


def GUI_Visualization():

    def LogView():
        print("ZAAAAAART")
        Display_Logs()

    root_new = tk.Toplevel()  #  Tk()
    root_new.title("VISUALIZATION")
    root_new.geometry("500x250")

    button_font = ("Arial", 14, "bold")

    # Load the icon image
    original_image = Image.open("Visualization.png")
    resized_image_3 = original_image.resize((125, 125))
    tk_image_3 = ImageTk.PhotoImage(resized_image_3)

    image_label = tk.Label(root_new, image=tk_image_3, width=250, height=250)  # type: ignore
    image_label.pack(side=tk.LEFT, padx=10)

    # Create a menu bar
    menu_bar = Menu(root_new)
    #
    # # Create a file menu and add it to the menu bar
    # file_menu = Menu(menu_bar, tearoff=0)
    # file_menu.add_command(label="Open")
    # file_menu.add_command(label="Save")
    #
    # menu_bar.add_cascade(label="File", menu=file_menu)
    #
    # # Create Visualization menu
    # vis_menu = Menu(menu_bar, tearoff=0)
    # vis_menu.add_command(label="View Logs", command = LogView)
    # # edit_menu.add_command(label="Copy")
    # # edit_menu.add_command(label="Paste")
    # menu_bar.add_cascade(label="Visualization", menu=vis_menu)
    #
    # Create an edit menu and add it to the menu bar
    exit_menu = Menu(menu_bar, tearoff=0)
    exit_menu.add_command(label="Exit", command=root_new.destroy)
    menu_bar.add_cascade(label="Exit", menu=exit_menu)
    #
    # Display the menu bar
    root_new.config(menu=menu_bar)
    #
    # # Create buttons and place them on the window
    button1 = tk.Button(
        root_new,
        text="Log Display",
        width=20,
        height=3,
        font=button_font,
        relief=tk.RAISED,
        command=LogView,
    )
    button1.pack(side=tk.LEFT, padx=10)

    # Start the main event loop
    root_new.mainloop()
