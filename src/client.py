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
import io 
import pygame
from pygame.locals import *

import preview
import inputController
import photo
from socketHelper import SH
import gifStitcher

class Client:
    SERVERADDRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
    KILLSCRIPT = False
    PRINTREMOTE = False 

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
        self.screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)

    def _worker(self):
        print("starting worker thread")
        while True:

            if (self.previewEvent.is_set()): #a
                self.previewEvent.print()
                self.requestPreview()
                self.inputControl.clearAllEvents()

            if (self.photoEvent.is_set()): #p
                self.photoEvent.print()
                self.requestPhotos()
                self.inputControl.clearAllEvents()

            if (self.reviewEvent.is_set()): #r
                self.reviewEvent.print()
                self.inputControl.clearAllEvents()

            time.sleep(0.3)

    def requestPreview(self):
        self.sendRequestToAllServers("preview")

        data = [None]*4
        preRes = photo.Photo.PRERES
        print(f"pre:{preRes}")
        while(self.previewEvent.is_set()):
            for i, sock in enumerate(self.sockets):
               data[i] = self.receiveBytes(sock)

            viewData = data[self.previewEvent.modifierState]
            print(f"finalsize: {sys.getsizeof(viewData)}")
            img = pygame.image.frombuffer(viewData, preRes, 'RGB')
            self.screen.blit(img, preRes)
            pygame.display.update()

    def requestPhotos(self):
        def _receivephoto(self, sock, photoList):
            photoList.append(self.recieveBytes(sock))

        time.sleep(2)
        self.sendRequestToAllServers("photo")
        threads = []
        photoList = []
        for sock in self.sockets:
            writeThread = threading.Thread(target = _receivephoto, args=(sock,photoList))
            writeThread.start()
            threads.append(writeThread)
        for thred in threads:
            thred.join()

        photoList.sort()
        gifStitcher.stitch(photoList, "newGif")


    def receiveBytes(self, sock):
        print(f"RECEIVING DATA: {sock.getsockname()[1]}" )
        dataArray = None
        with io.BytesIO() as data:
            rawData = sock.recv(SH.REQUESTSIZE)
            dataSize = SH.unpadBytes(rawData)
            blockSize = 2048 
            
            print("RBexpectedSize")
            print(dataSize)

            #TODO: MAKE THIS FUCKING THING READ THE RIGHT NUMBER OF BYTES
            while(data.tell() <= dataSize):
                data.write(sock.recv(blockSize))

            data.seek(0)
            dataArray = data.read()
            print("RBfinalreceivedSIZE")
            print(sys.getsizeof(dataArray))
        return dataArray 

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
            return 
        for address in self.SERVERADDRESSES:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(hostname = address)
            self.ssh.append(ssh)

        if self.KILLSCRIPT: 
            self.sendCommandToAllServers("killall -9  python3")
        self.sendCommandToAllServers(command, self.PRINTREMOTE)

    def closeServers(self):
        self.sendCommandToAllServers("killall -9 python3")
        for sock in self.sockets:
            sock.close()
        for ssh in self.ssh: 
            ssh.close()
            print(f"server: {ssh} has been terminated")
        
    def sendCommandToAllServers(self, command, printOutputAsync = False):
        print("SENDING COMMAND")
        for ssh in self.ssh:
            print(f"COMMAND: {command}: {ssh}")
            stdin, stdout, stderr = ssh.exec_command(command)# get_pty=True)
            if printOutputAsync:
                print("printing")
                printThread = threading.Thread(target = self._printSSHCommand, args = [stdout], daemon = True)
                printThread.start()
                self.debugThreads.append(printThread)

    #https://stackoverflow.com/questions/25260088/paramiko-with-continuous-stdout
    def _printSSHCommand(self, stdout):
        print(f"started printing {stdout}")
        while(stdout.closed != True):
            print("        REMOTE:" + stdout.readline())

    def sendRequestToAllServers(self, request):
        for sock in self.sockets:
            name = sock.getsockname()
            print(f"requesting {request}: {name[0], name[1]}" )
            sock.sendall(SH.padBytes(f"{request}"))



