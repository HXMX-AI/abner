from importlib.metadata import version


def Check_Version(moduleName):
    ver = version(moduleName)
    print(ver)
    return ver


if __name__ == "__main__":

    moduleName = input("Enter module name: ")
    ver = Check_Version(moduleName)
