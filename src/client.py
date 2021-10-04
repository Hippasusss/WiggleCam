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
import os

import preview
import inputController
from socketHelper import SH
import gifStitcher

class Client:
    SERVERADDRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]

    def __init__(self):
        warnings.filterwarnings("ignore") 
        self.ADDRESS = "172.19.181.254"
        self.PORTS = ("5555", "5556", "5557", "5558")
        self.PREVIEWPORTS = ("5559", "5560", "5561", "5562")
        self.inputControl = inputController.Input()
        self.ssh = []
        self.sockets = []

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

        self.connectToServers()

        #Start worker thread running
        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print("starting worker thread")
        while True:

            if (self.previewEvent.is_set()): #a
                self.previewEvent.print()
                print("previewing")
                self.requestPreview()
                self.previewWindow.startPreview(SH.CLIENTIP, self.PREVIEWPORTS)
                # tell minis to start sending video
                print("stopping preview")
                self.previewWindow.stopPreview()
                self.requestPreview()
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

    def requestPreview(self):
        print("")
        print("REQUESTING PREVIEW")
        self.sendRequestToAllServers("preview")


    def requestPhotos(self):
        print("")
        print("REQUESTING PHOTO")
        self.sendRequestToAllServers("photo")

        threads = []
        print("")
        print("STARTING RECEIVE THREADS")
        photoList =[]
        for sock in self.sockets:
            writeThread = threading.Thread(target = self._receivephoto, args=(sock,photoList))
            writeThread.start()
            print(f"started thread: {writeThread}")
            threads.append(writeThread)
        for thred in threads:
            thred.join()

        print("PHOTO COMPLETE")
        print("")

        print("CREATING GIF")
        print("")
        photoList.sort()
        gifStitcher.stitch(photoList, "newGif")

    def _receivephoto(self, sock, photoList):
        returndata = self.receiveDataFromServer(sock)
        if returndata == "incorrect":
            print("Server Shat It")
            return
        filepath, filesize = returndata.split(":")
        filename = os.path.basename(filepath)
        filesize = int(filesize)

        print(f"Receiving:{filename} {filesize}")
        blockSize = filesize
        with open(filename , "wb") as f:
            photoList.append(f.name)
            while True:
                print(f"Receiving: {filename}")
                block = sock.recv(blockSize)
                if not block:
                    f.close()
                    break
                if f.tell() >= filesize:
                    f.close()
                    break
                f.write(block)    
        print(f"finished: {filename}")

    def connectToServers(self):
        i = 0
        for port in self.PORTS:
            address = self.SERVERADDRESSES[i]
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connected = False
            while not connected:
                try:
                    sock.connect((address, int(port)))
                    print(f"connection to {i} successfull")
                    connected = True
                except:
                    print(f"waiting for connection on {i}. Trying again....")
                    time.sleep(1)
            self.sockets.append(sock)
            i+=1


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

        #self.sendCommandToAllServers("killall -9  python3")
        self.sendCommandToAllServers(command)

    def closeServers(self):
        self.sendCommandToAllServers("killall -9 python3")
        for sock in self.sockets:
            sock.close()
        for ssh in self.ssh: 
            ssh.close()
            print(f"server: {ssh} has been terminated")
        
    def sendCommandToAllServers(self, command):
        print("")
        print("SENDING COMMAND")
        for ssh in self.ssh:
            print(f"COMMAND: {command}: {ssh}")
            ssh.exec_command(command)
        print("")
        
    def sendRequestToAllServers(self, request):
        for sock in self.sockets:
            name = sock.getsockname()
            print(f"requesting preview: {name[0], name[1]}" )
            sock.sendall(SH.padBytes(f"{request}"))

    def receiveDataFromServer(self, sock):
        print(" " )
        print(f"RECEIVING DATA: sock.getsockname()[1]" )
        rawData = sock.recv(SH.REQUESTSIZE)
        returndata = SH.unpadBytes(rawData)
        print(f"rawsize: {len(rawData)}" )
        print(f"stripsize: {len(returndata)}" )
        print(f"rawData: {repr(rawData)}" )
        print(f"data: {returndata}" )
        print(" " )
        return returndata


