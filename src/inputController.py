from getkey import getkey, keys
import threading
import time

# reveive input from camera and send to other threads to perform tasks
class Input:
    events = []

    def startChecking(self):
        inputThread = threading.Thread(target = self._checkInput, daemon = True)
        inputThread.start()

    def _checkInput(self):
        print("starting input thread")
        waitingEvent = None
        while (True):
            keyInput = getkey() 
            print("input =============================================")
            print("keyInput: {0}".format(keyInput))
            for event in self.events: 
                if event.key == keyInput:
                    if waitingEvent is None:
                        print("setting: {0} from input {1}".format(event.key, keyInput))
                        event.set()
                        if event.isToggle: 
                            print("Toggle On")
                            waitingEvent = event
                    elif event is waitingEvent:
                        event.clear()
                        print("Toggle Off")
                        waitingEvent = None
                    else:
                        print("blocked. waiting for {0}".format(waitingEvent.key))
            print("input =============================================")

    def addEvent(self, keyEvent):
        self.events.append(keyEvent)

    def clearAllEvents(self):
        for event in self.events:
            event.clear()

class KeyEvent:
    event = None
    key = None
    isToggle = False

    def __init__(self, keyCode, isToggle = False):
        self.key = keyCode
        self.isToggle = isToggle
        self.event = threading.Event()
        self.clear()

    def set(self):
        if not self.event.is_set():
            self.event.set()
        self.print()

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

    def print(self):
        print("{0}: {1}".format(self.key, self.is_set()))

