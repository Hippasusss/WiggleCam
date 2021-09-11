from vidgear.gears import NetGear 
from getkey import getkey, keys
from enum import Enum

import cv2
import threading
import time
import subprocess
import socket
import sys 

import preview
import inputController

#CONTROLLER

# client side controller of everything 
class Client:
    SERVERADDRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]

    def __init__(self, ADDRESS, PORT):
        self.ADDRESS = ADDRESS
        self.PORT = PORT
        self.inputControl = inputController.Input()
        self.ssh = []

        self.previewEvent = inputController.KeyEvent('a', isToggle = True)
        self.reviewEvent  = inputController.KeyEvent('r', isToggle = True)
        self.photoEvent   = inputController.KeyEvent('p')
        self.previewWindow = preview.Preview(receiveMode = True, event = self.previewEvent)

        # Register input events and start input thread running
        self.inputControl.addEvent(self.previewEvent)
        self.inputControl.addEvent(self.photoEvent)
        self.inputControl.addEvent(self.reviewEvent)
        self.inputControl.startChecking()

        # Start the scripts running on the PI zeros
        self.startServers()

        #Start worker thread running
        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print("starting worker thread")
        while True:
            if (self.previewEvent.is_set()): #a
                self.previewEvent.print()
                print("previewing")
                self.previewWindow.startPreview(self.ADDRESS, self.PORT)
                # tell minis to start sending video
                print("stopping preview")
                self.previewWindow.stopPreview()
                self.inputControl.clearAllEvents()

            if (self.photoEvent.is_set()): #p
                self.photoEvent.print()
                print("taking photo")
                self.requestPhotos()
                # tell minis to take a photo
                self.inputControl.clearAllEvents()

            if (self.reviewEvent.is_set()): #r
                self.reviewEvent.print()
                print("looking at photos")
                while(self.reviewEvent.is_set()):
                    continue
                # display gifs that have been taken
                print("finished looking at photos")
                self.inputControl.clearAllEvents()

            print(self.ssh)
            time.sleep(0.3)

    def requestPhotos(self):
        i = 0
        for port in self.PORT:
            address = self.SERVERADDRESSES[i]
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.connect((address, int(port)))
                except ConnectionRefusedError:
                    print("Connection Refused")
                    break
                print("connecting to port: " + port)
                print("sending request...")
                sock.sendall(bytes("photo", "utf-8"))


                filename, filesize = sock.recv(1024).decode().split(":")
                filename = os.path.basename(filename)
                filesize = int(filesize)

                print(f"Receiving:{filename} {filesize}")
                count = 0;
                with open(filename + str(port), "wb") as f:
                    while True:
                        print(f"Receiving:{filename}: {count} bytes")
                        count = count + 1024
                        block = sock.recv(1024)
                        if not block:
                            break
                        f.write(block)
                sock.close()
                i += 1

    def startServers(self):
        command = "python3 ~/script/WiggleCam/src/cameraModule.py"
        if len(self.ssh) is not 0:
            print("ssh subprocesses already running")
            return 
        for address in self.SERVERADDRESSES:
            subprocess.run(["ssh", address, "killall python3;", command])

        sendCommandToAllServers()
        #self.sendCommandToAllServers(command)

    def closeServers(self):
        self.sendCommandToAllServers("killall python3")
        for p in self.ssh: 
            p.terminate()
            print(f"server: {p} has been terminated")
        
    def sendCommandToAllServers(self, command):
        for p in self.ssh:
            print(f"COMMAND: {command}: {p}")
            p.communicate(command)
        
