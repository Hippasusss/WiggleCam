from getkey import getkey, keys
import threading
import time

# reveive input from camera and send to other threads to perform tasks
class Input:

    inputThread = None
    events = []


    def startChecking(self):
        if (self.inputThread is None):
            self.inputThread = threading.Thread(target = self._checkInput, daemon = True)
            self.inputThread.start()

    def _checkInput(self):
        waitingEvent = None
        while (True):
            time.sleep(0.1)
            keyInput = getkey() 
            for event in self.events:
                if(event.key == keyInput and waitingEvent is None):
                    print(event)
                    event.set()
                    waitingEvent = event
                elif event.key == waitingEvent:
                    event.clear()
                    waitingEvent = None

    def addEvent(self, keyEvent):
        self.events.append(keyEvent)

class KeyEvent:
    event = threading.Event()
    key = None
    isToggle = False


    def __init__(self, keyCode, isToggle = False):
        self.key = keyCode

    def set(self):
        if self.isToggle:
            self.toggle()
            return

        if not self.event.is_set():
            self.event.set()

    def clear(self):
        if self.event.is_set():
            self.event.clear()

    def toggle(self):
        if not self.event.is_set():
            self.event.set()
        elif self.event.is_set():
            self.event.clear()

    def is_set(self):
        return self.event.is_set()

