from vidgear.gears import NetGear 
from getkey import getkey, keys
from enum import Enum

import cv2
import threading

import preview
import inputController

#CONTROLLER

# client side controller of everything 
class State(Enum):
    idle = 0
    preview = 1
    photo = 2

class Client:

    PORT = None
    ADDRESS = None

    state = State.idle
    inputControl = inputController.Input()

    # INPUT EVENTS
    previewEvent = inputController.KeyEvent('a', isToggle = True)
    photoEvent = inputController.KeyEvent('p')
    reviewEvent = inputController.KeyEvent('r', isToggle = True)

    previewWindow = preview.Preview(receiveMode = True, event = previewEvent)

    def __init__(self, ADDRESS, PORT):
        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()
        self.ADDRESS = ADDRESS
        self.PORT = PORT
        self.inputControl.addEvent(self.previewEvent)
        self.inputControl.addEvent(self.photoEvent)
        self.inputControl.addEvent(self.reviewEvent)
        self.inputControl.startChecking()

    def _worker(self):
        while True:
            if (self.previewEvent.is_set() and self.state is State.idle):
                print("previewing")
                self.state = State.preview
                self.previewWindow.startPreview(self.ADDRESS, self.PORT)
                # tell minis to start sending video
                print("stopping preview")
                self.state = State.idle
                self.previewWindow.stopPreview()

            if (self.photoEvent.is_set() and self.state is State.idle):
                print("taking photo")
                self.state = State.photo
                # tell minis to take a photo
                print("finished photo")
                self.state = State.idle

            if (self.reviewEvent.is_set() and self.state is State.idle):
                print("looking at photos")

