import pickle


def Read_Pickle_File(pckFileName):

    with open(pckFileName, "rb") as file:
        pckObj = pickle.load(file)

    return pckObj
