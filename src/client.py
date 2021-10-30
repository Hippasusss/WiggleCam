from getkey import getkey, keys
import threading
import time
import socket
import sys 
import paramiko
import os
import io 
import pygame

from socketHelper import SH
import inputController
import gifStitcher
import photo

class Client:
    SERVERADDRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
    KILLSCRIPT =False 
    PRINTREMOTE = False

    def __init__(self):
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
        # Create the socket connections to the PI Zeros
        self.connectToServers()

        #Start worker thread running
        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

        # Init pygame and screen
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((640,480), pygame.RESIZABLE)

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
        while(self.previewEvent.is_set()):
            for i, sock in enumerate(self.sockets):
               data[i] = SH.receiveBytes(sock)
            viewData = data[self.previewEvent.modifierState]
            print(len(data))
            img = pygame.image.frombuffer(viewData, preRes, 'RGB')
            self.screen.blit(img, (0,0))
            pygame.display.update()

    def requestPhotos(self):
        def _receivephoto(self, sock, photoList):
            photoList.append(SH.receiveBytes(sock))
        self.sendRequestToAllServers("photo")
        threads = []
        photoList = []
        for sock in self.sockets:
            writeThread = threading.Thread(target = _receivephoto, args=(self, sock, photoList))
            writeThread.start()
            threads.append(writeThread)
        for thred in threads:
            thred.join()
        photoList.sort()
        gifStitcher.stitch(photoList, "newGif")

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
                except:
                    print(f"waiting for connection on {i + 1}. Trying again....")
                    time.sleep(1)
            self.sockets.append(sock)

    def startServers(self):
        command = "python3 -u ~/script/WiggleCam/src/cameraModule.py 2>&1"
        for address in self.SERVERADDRESSES:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(hostname = address)
            self.ssh.append(ssh)
        if self.KILLSCRIPT: 
            self.sendCommandToAllServers("killall -9  python3")
            time.sleep(0.1)
        self.sendCommandToAllServers(command, self.PRINTREMOTE)

    def closeServers(self):
        self.sendCommandToAllServers("killall -9  python3")
        for sock in self.sockets:
            sock.close()
        for ssh in self.ssh:
            ssh.close()

    def sendCommandToAllServers(self, command, printOutputAsync = False):
        def _printSSHCommand(stdout):
            while(stdout.closed != True):
                print("REMOTE:" + stdout.readline())
        print(f"SENDING COMMAND TO ALL: {command}")
        for ssh in self.ssh:
            stdin, stdout, stderr = ssh.exec_command(command)
            if printOutputAsync:
                printThread = threading.Thread(target = _printSSHCommand, args = [stdout], daemon = True)
                printThread.start()
                self.debugThreads.append(printThread)

    def sendRequestToAllServers(self, request):
        print(f"requesting {request}")
        for sock in self.sockets:
            SH.sendBytes(sock, f"{request}".encode(encoding=SH.ENCODETYPE))



