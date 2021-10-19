from getkey import getkey, keys
from enum import Enum

import warnings
import cv2
import threading
import time
import socket
import sys 
import paramiko
import os
from pygame.locals import *

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
        self.debugThreads = []

        self.previewEvent = inputController.KeyEvent('a', isToggle = True, modifiers = ["1", "2", "3", "4", "5"])
        self.reviewEvent  = inputController.KeyEvent('r', isToggle = True)
        self.photoEvent   = inputController.KeyEvent('p')

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

        # Init pygame and screen
        pygame.init()
        pygame.mouse.set_visible(False)
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        if img is None or img.get_height() < 240: # Letterbox, clear background
            screen.fill(0)
        if img:
            screen.blit(img, ((320 - img.get_width() ) / 2, (240 - img.get_height()) / 2))

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
                print("taking photo")
                self.photoEvent.print()
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
        time.sleep(2)
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
        for i, port in enumerate(self.PORTS):
            address = self.SERVERADDRESSES[i]
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connected = False
            while not connected:
                try:
                    sock.connect((address, int(port)))
                    print(f"connection to {i + 1} successfull")
                    connected = True
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    print(f"waiting for connection on {i + 1}. Trying again....")
                    print(self.ssh[i])
                    time.sleep(1)
            self.sockets.append(sock)


    def startServers(self):
        command = "python3 -u ~/script/WiggleCam/src/cameraModule.py 2>&1"
         
        if len(self.ssh) is not 0:
            print("ssh subprocesses already running")
            return 
        for address in self.SERVERADDRESSES:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(hostname = address)
            self.ssh.append(ssh)

        self.sendCommandToAllServers("killall -9  python3")
        self.sendCommandToAllServers(command, True)

    def closeServers(self):
        self.sendCommandToAllServers("killall -9 python3")
        for sock in self.sockets:
            sock.close()
        for ssh in self.ssh: 
            ssh.close()
            print(f"server: {ssh} has been terminated")
        
    def sendCommandToAllServers(self, command, printOutputAsync = False):
        print("")
        print("SENDING COMMAND")
        for ssh in self.ssh:
            print(f"COMMAND: {command}: {ssh}")
            stdin, stdout, stderr = ssh.exec_command(command)# get_pty=True)
            if printOutputAsync:
                print("printing")
                printThread = threading.Thread(target = self.printSSHCommand, args = [stdout], daemon = True)
                printThread.start()
                self.debugThreads.append(printThread)
        print("")
        

    #https://stackoverflow.com/questions/25260088/paramiko-with-continuous-stdout
    def printSSHCommand(self, stdout):
        print(f"started printing {stdout}")
        while(stdout.closed != True):
            print("        REMOTE:" + stdout.readline())


    def sendRequestToAllServers(self, request):
        for sock in self.sockets:
            name = sock.getsockname()
            print(f"requesting {request}: {name[0], name[1]}" )
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


