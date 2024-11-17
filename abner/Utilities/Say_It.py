import pyttsx3

#========================================
def Say_It(message='WARNING', rate=150):

    engine = pyttsx3.init()
    engine.setProperty('rate', rate )
    engine.say(message)
    print(message)
    engine.runAndWait()

#=======================================
if __name__ == "__main__":

    Say_It('The file does not exist, pick another one')
