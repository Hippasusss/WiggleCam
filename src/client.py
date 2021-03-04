from vidgear.gears import NetGear 
from getkey import getkey, keys
from enum import Enum

import cv2
import threading
import time
import subprocess
import sys 

import preview
import inputController

#CONTROLLER

# client side controller of everything 
class Client:

    PORT = None
    ADDRESS = None
    SERVERADDRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]

    inputControl = inputController.Input()

    previewEvent = inputController.KeyEvent('a', isToggle = True)
    reviewEvent  = inputController.KeyEvent('r', isToggle = True)
    photoEvent   = inputController.KeyEvent('p')

    previewWindow = preview.Preview(receiveMode = True, event = previewEvent)

    def __init__(self, ADDRESS, PORT):
        self.ADDRESS = ADDRESS
        self.PORT = PORT

        #Start worker thread running
        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

        # Register input events and start input thread running
        self.inputControl.addEvent(self.previewEvent)
        self.inputControl.addEvent(self.photoEvent)
        self.inputControl.addEvent(self.reviewEvent)
        self.inputControl.startChecking()

        # Start the scripts running on the PI zerosj
        self.startServers()

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

    def startServers(self):
        command = "python3 ~/script/WiggleCam/src/cameraModule.py"
        self.sendCommandToAllServers(command)

    def closeServers(self):
        command = "close all the servers please"
        self.sendCommandToAllServers(command)
        
    def sendCommandToAllServers(self, command):
        for address in self.SERVERADDRESSES:
            ssh = subprocess.run(["ssh", address, command])
        
