"""
    Creates a new project folder in the dir_PROJECTS folder
    Creates sub folders Input_Data and Debug
    Copies Path. cwd(). parent / "Config_Files" / "config_logRcnd.xlsx" to the project folder
    Creates a project object and saves it to the project folder in a pickle file

"""

from pathlib import Path
from shutil import copy

from abner.Classes.Class_Project import Project
from abner.Utilities.FilesInDir import FilesInDir
from abner.Utilities.Say_It import Say_It


def Create_Prj(dir_PROJECTS, project_name):

    # Does dir_projects exist?
    if not dir_PROJECTS.is_dir():
        print("No directory for PROJECTS, Create the directory for projects first")
        return "Incomplete"
    elif dir_PROJECTS.is_dir():
        dir_prj = dir_PROJECTS / project_name

        try:
            dir_prj.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            Say_It("WARNING: Project Already exists")
            print(f"Project  {dir_prj}  already exists, What are you trying to do?")
        else:
            print(f" Project {dir_prj}  was created")
            (dir_prj / "Input_Data").mkdir(parents=True, exist_ok=False)
            (dir_prj / "Debug").mkdir(parents=True, exist_ok=False)
            (dir_prj / "Output_Data").mkdir(parents=True, exist_ok=False)
            (dir_prj / "Visuals").mkdir(parents=True, exist_ok=False)

            # config file COPY
            file_config = Path.cwd().parent / "Config_Files" / "config_logRcnd.xlsx"
            copy(file_config, dir_prj)

            # Scheduler COPY
            file_scheduler = Path.cwd().parent / "Config_Files" / "Scheduler.xlsx"
            copy(file_scheduler, dir_prj)

            # Move templates to cwd/Visualization folder
            path_source_visuals = Path.cwd().parent / "Config_Files"
            all_files = FilesInDir(path_source_visuals, "xlsx")

            if not all_files:
                raise ValueError("No Visualization templates found")

            path_dest_visuals = dir_prj / "Visuals"
            [
                copy(path, path_dest_visuals)
                for path in all_files
                if path.stem.startswith("Log_Template")
            ]

            # CREATE a project object and save it to the project folder
            Prj = Project(dir_prj, project_name)
            Prj.Save2Pck()


if __name__ == "__main__":

    dir_PROJECTS = Path("C:/Users/ridva/OneDrive/Documents/WELLS")
    project_name = "Junk_Nov14_test"  #     ND_152N_101W_20241004_LAS_test"

    output = Create_Prj(dir_PROJECTS, project_name)
    print("done")