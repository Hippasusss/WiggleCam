from vidgear.gears import NetGear 
from getkey import getkey, keys
from enum import Enum

import warnings
import cv2
import threading
import time
import subprocess
import socket
import sys 
import paramiko

import preview
import inputController

#CONTROLLER

# client side controller of everything 
class Client:
    SERVERADDRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
    #SERVERADDRESSES = [ "p1", "p2", "p3", "p4" ]

    def __init__(self, ADDRESS, PORT):
        warnings.filterwarnings("ignore") 
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
                # tell the minis to stop
                self.inputControl.clearAllEvents()

            if (self.photoEvent.is_set()): #p
                self.photoEvent.print()
                print("taking photo")
                self.requestPhotos()
                self.inputControl.clearAllEvents()

            if (self.reviewEvent.is_set()): #r
                self.reviewEvent.print()
                print("looking at photos")
                while(self.reviewEvent.is_set()):
                    continue
                # display gifs that have been taken
                print("finished looking at photos")
                self.inputControl.clearAllEvents()
            #print(time.asctime(time.localtime()))
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
        command = "python3 ~/script/WiggleCam/src/cameraModule.py &"
        if len(self.ssh) is not 0:
            print("ssh subprocesses already running")
            return 
        for address in self.SERVERADDRESSES:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(hostname = address)
            self.ssh.append(ssh)

        self.sendCommandToAllServers("killall -9  python3")
        self.sendCommandToAllServers(command)

    def closeServers(self):
        self.sendCommandToAllServers("killall -9 python3")
        for ssh in self.ssh: 
            ssh.close()
            print(f"server: {ssh} has been terminated")
        
    def sendCommandToAllServers(self, command):
        print("")
        print("INPUT")
        for ssh in self.ssh:
            print(f"COMMAND: {command}: {ssh}")
            ssh.exec_command(command)

        
