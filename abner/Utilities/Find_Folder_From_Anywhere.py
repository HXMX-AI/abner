import os


# =================================================================
def Find_Folder_From_Anywhere(folder_name, search_path="/"):

    print("BE PATIENT: SEARCHING .....")
    for root, dirs, files in os.walk(search_path):
        if folder_name in dirs:
            return os.path.join(root, folder_name)
    return None


# =================================================================
if __name__ == "__main__":

    folder_name = "WELLS"
    result = Find_Folder_From_Anywhere(folder_name)

    if result:
        print(f"Folder found at: {result}")
    else:
        print("Folder not found.")
