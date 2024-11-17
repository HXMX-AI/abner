import  os
import  glob
from    Utilities.Say_It        import      Say_It
from    pathlib                 import      Path

#==================================================
# def FilesInDir(folderPath, extensions = 'pck'):
#
#     # Must be Path object
#     if isinstance(folderPath, Path):
#         dir = folderPath
#     else:
#         dir = Path(folderPath)
#
#     # extensions must be  list
#     if isinstance(extensions, str):
#         extensions = [extensions]
#     elif isinstance(extensions, list):
#         pass
#     else:
#         print('extensions must be either a string or a list')
#         print('Crashing')
#
#     isDir = dir.is_dir()
#     if not isDir:
#         Say_It('Warning, see message', 150)
#         print('Directory   ' + str(folderPath) + '   does NOT exist, try again')
#         return None
#     else:
#         all_files = []
#         for ext in extensions:
#             temp_files     = list(dir.glob("*.*"))
#             matching_files = [p for p in temp_files if p.suffix == '.' + ext]
#             if len(matching_files) == 0 :
#                 print(f'No files with extension {ext} was found in {dir}' )
#             all_files  = all_files + matching_files
#             if False: print(f'Num files in temp-files {len(matching_files)}')
#
#         if len(all_files) ==  0:
#             print(f'No files found with extension  .{extensions}   in directory  {folderPath}')
#
#         return  all_files

#==================================================
def FilesInDir(folderPath, extensions = 'pck'):

    # Must be Path object
    if isinstance(folderPath, Path):
        dir = folderPath
    else:
        dir = Path(folderPath)

    # extensions must be  list
    if isinstance(extensions, str):
        extensions = [extensions]
    elif isinstance(extensions, list):
        pass
    else:
        print('extensions must be either a string or a list')
        print('Crashing')

    isDir = dir.is_dir()
    if not isDir:
        Say_It('Warning, see message', 150)
        print('Directory   ' + str(folderPath) + '   does NOT exist, try again')
        return None
    else:
        all_files = []
        for ext in extensions:
            search_extension = '*.'+ext
            # temp_files     = list(dir.glob("*.*"))
            # matching_files = [p for p in temp_files if p.suffix == '.' + ext]
            matching_files = list(dir.glob(search_extension))
            if len(matching_files) == 0 :
                print(f'No files with extension {ext} was found in {dir}' )
            all_files  = all_files + matching_files
            if False: print(f'Num files in temp-files {len(matching_files)}')

        if len(all_files) ==  0:
            print(f'No files found with extension  .{extensions}   in directory  {folderPath}')

        return  all_files


#==========================================================
if __name__ == "__main__":

    extensions = ['las']     #  ['log.pck']    # ['las','csv', 'pck']
    #dir_prj    = "C:\\Users\\ridva\\OneDrive\\Documents\\WELLS\\Groningen_test\\Input"
    dir_prj    = "C:/Users/ridva/OneDrive/Documents/WELLS/Groningen_test/Input"
    files      = FilesInDir(dir_prj, extensions)

    if False:
        if files  is not None:
            print(f'\nTotal of {len(files)} in {dir_prj}\n')
            [print(s, end= '\n')  for s in files]