from getkey import getkey, keys
import threading

# reveive input from camera and send to other threads to perform tasks
class Input:

    inputThread = None
    keyInput = None

    photoEvent = threading.Event()
    previewEvent = threading.Event()
    exitEvent = threading.Event()

    def __init__(self):
        self.keyInput = getkey()
        self.startChecking()

    def startChecking(self):
        if (self.inputThread is None):
            self.inputThread = threading.Thread(target = self.checkInput, daemon = True)
            self.inputThread.start()
        

    def _checkInput(self):

        eventDict = { 
            keys.A : photoEvent, 
            keys.P : previewEvent, 
            keys.Q : exitEvent
        }

        while (True):
            inputThread.sleep(0.1)
            eventDict[self.keyInput].set()

            # # take a photo
            # if (self.keyInput == keys.A):
            #     continue

            # # start preview 
            # if (self.keyInput == keys.P):
            #     continue

            # # quit
            # if (self.keyInput == keys.Q):
            #     continue
