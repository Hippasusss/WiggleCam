from getkey import getkey, keys
import threading

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
            Input = getkey()
            print("input =============================================")
            print(f"keyInput: {Input}")
            for event in self.events:
                if event.check(Input):
                    if waitingEvent is None:
                        print(f"setting: {event.key} from input {Input}")
                        event.set()
                        if event.isToggle:
                            print("Toggle On")
                            waitingEvent = event
                    elif event is waitingEvent:
                        event.clear()
                        print("Toggle Off")
                        waitingEvent = None
                    else:
                        print(f"blocked. waiting for {waitingEvent.key}")
                elif waitingEvent is not None and waitingEvent.checkModifier(Input):
                    waitingEvent.setModifierState(Input)
                    print(f"Modifier input. setting event {waitingEvent.key} to current state of {Input}")
            print("input =============================================")


    def addEvent(self, keyEvent):
        self.events.append(keyEvent)

    def clearAllEvents(self):
        for event in self.events:
            event.clear()

class KeyEvent:

    def __init__(self, keyCode, callback, isToggle = False, modifiers = [] ):
        self.callback = callback
        self.key = keyCode
        self.isToggle = isToggle
        self.event = threading.Event()
        self.modifiers = modifiers
        self.modifierState = 1
        self.clear()

    def set(self):
        if not self.event.is_set():
            self.callback()
            self.event.set()
        self.print()

    def setModifierState(self, setVar):
        print(self.modifierState)
        self.modifierState = int(setVar)

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

    def check(self, check):
        return self.key == check

    def checkModifier(self, check):
        return check in self.modifiers and not (int(check) == self.modifierState)

    def print(self):
        print("{0}: {1}".format(self.key, self.is_set()))

