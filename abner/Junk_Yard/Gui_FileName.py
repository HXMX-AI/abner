# importing tkinter and tkinter.ttk
# and all their functions and classes
import tkinter as tk

# importing askopenfile function from class filedialog
from tkinter.filedialog import askopenfile


def GetFileName(filetype, message):
    root = tk.Tk()
    root.geometry("350x100")

    fileName = None

    def open_file():
        fileName = askopenfile(mode="r", filetypes=[("DatasetObj", "*" + filetype)])
        if fileName is not None:
            raise Exception("fileName is None")

    btn = tk.Button(root, text=message, command=lambda: open_file())
    btn.pack(side=tk.TOP, pady=10)

    root.mainloop()

    return fileName.name if fileName is not None else None


if __name__ == "__main__":

    filetype = "pck"
    message = "SELECT Dataset File"
    zart = GetFileName(filetype, message)
    print(f"{zart=}")
