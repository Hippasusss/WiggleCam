from getkey import getkey, keys
import threading
import time

# reveive input from camera and send to other threads to perform tasks
class Input:

    inputThread = None
    keyInput = None

    events = []

    def __init__(self):
        self.keyInput = getkey()

    def startChecking(self):
        if (self.inputThread is None):
            self.inputThread = threading.Thread(target = self.checkInput, daemon = True)
            self.inputThread.start()
        

    def _checkInput(self):
        while (True):
            time.sleep(0.1)
            for event in events:
                if(event.key == keyInput):
                    event.event.set()


    def addEvent(keyCode):
        events.add(KeyEvent(keycode))

class KeyEvent:
    event = threading.Event()
    key = None

    def __init__(self, keyCode):
        self.key = keyCode
        self.name = name

