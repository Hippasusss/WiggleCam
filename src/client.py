from vidgear.gears import NetGear 
from getkey import getkey, keys
from enum import Enum

import cv2
import threading
import time

import preview
import inputController

#CONTROLLER

# client side controller of everything 
class Client:

    PORT = None
    ADDRESS = None

    inputControl = inputController.Input()

    # INPUT EVENTS
    previewEvent = inputController.KeyEvent('a', isToggle = True)
    reviewEvent  = inputController.KeyEvent('r', isToggle = True)
    photoEvent   = inputController.KeyEvent('p')

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
        print("starting worker thread")
        while True:
            if (self.previewEvent.is_set()):
                self.previewEvent.print()
                self.reviewEvent.print()
                self.photoEvent.print()
                print("previewing")
                self.previewWindow.startPreview(self.ADDRESS, self.PORT)
                # tell minis to start sending video
                print("stopping preview")
                self.previewWindow.stopPreview()
                self.inputControl.clearAllEvents()

            if (self.photoEvent.is_set()):
                self.photoEvent.print()
                print("taking photo")
                # tell minis to take a photo
                self.inputControl.clearAllEvents()

            if (self.reviewEvent.is_set()):
                self.reviewEvent.print()
                print("looking at photos")
                while(self.reviewEvent.is_set()):
                    continue
                # display gifs that have been taken
                print("finished looking at photos")
                self.inputControl.clearAllEvents()

            time.sleep(0.3)
            print("worker idle...")

