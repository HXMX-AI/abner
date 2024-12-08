import  os


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



    def Add_Prefix(self,s):
        newName = os.path.join(self.dirName, s + '_' + self.fileName)
        return newName

    def Add_Suffix(self,s):
        newName = os.path.join(self.dirName, self.justName + '_' + s + '.'+ self.extName)
        return newName

    @staticmethod
    def Prefix(fileName, prefix):
        whatever = FileName(fileName)
        newName  = os.path.join(whatever.dirName, prefix + '_' + whatever.fileName)
        return newName

    @staticmethod
    def Suffix(fileName, suffix):
        whatever = FileName(fileName)
        newName  = os.path.join(whatever.dirName, whatever.justName + '_' + suffix + '.'+ whatever.extName)
        return newName




