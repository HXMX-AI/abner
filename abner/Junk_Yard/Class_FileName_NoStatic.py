import  os
import  pandas                              as          pd
from    GUIs.GUI_GetFileName                import      GetFileName


#================================================================
class FileName:

    slots = ['sep','altsep','extsep','absName','dirName','fileName','justName','extName']

    def __init__(self, inputName):
        os_sep, os_altsep, os_extsep = os.sep, os.altsep, os.extsep

        self.inputName = inputName
        self.sep       = os.sep
        self.altsep    = os.altsep
        self.extsep    = os.extsep
        self.absPath   = os.path.abspath(inputName)
        self.dirName   = os.path.dirname(self.absPath)

        temp          = self.absPath.split(os_sep)
        self.fileName = temp[-1]
        temp          = self.fileName.split(os_extsep)
        self.justName = temp[0]
        self.extName  = temp[1]

    def Add_Prefix(self, s):
        newName = os.path.join(self.dirName, s+'_' + self.fileName)
        return newName

    def Add_Suffix(self,s):
        newName = os.path.join(self.dirName, self.justName + '_' + s + '.'+ self.extName)
        return newName






#-----------------------------------------------------------------------------
if __name__ == '__main__':

    choice = 2
    match choice:
        case 1:
            fName = GetFileName('all')
        case 2:
            fName = "C:/Users/ridva/OneDrive/Documents/WELLS/Log_Template_0.xlsx"
        case 3:
            print('Will not work')
            fName = "WELLS/Log_Template_0.xlsx"
        case 4:
            print('will not work')
            fName = "\\C:WELLS\\Log_Template_0.xlsx"



    obj     = FileName(fName)
    sufName = obj.Add_Suffix('zart')
    preName = obj.Add_Prefix('zurt')
    print('done')
