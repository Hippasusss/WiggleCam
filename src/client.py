from getkey import getkey, keys

import threading
import time
import socket
import sys 
import paramiko
import os
import io 
import cv2
import numpy 

from socketHelper import SH
import inputController
import gifStitcher
import photo

class Client:
    KILLSCRIPT = True 
    PRINTREMOTE = False

    def __init__(self):
        self.ADDRESS = "172.19.181.254"
        self.SERVERADDRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
        self.PHOTOPORTS = ("5555", "5556", "5557", "5558")
        self.PREVIEWPORTS = ("5559", "5560", "5561", "5562")

        self.photosockets = []
        self.previewsockets = []
        self.ssh = []
        self.debugThreads = []
        self.previewThread = None

        # Register input events and start input thread running
        self.inputControl = inputController.Input()
        self.previewEvent = inputController.KeyEvent('a', isToggle = True, modifiers = ["1", "2", "3", "4", "5"])
        self.photoEvent   = inputController.KeyEvent('p')
        self.inputControl.addEvent(self.previewEvent)
        self.inputControl.addEvent(self.photoEvent)
        self.inputControl.startChecking()

        # Start the scripts running on the PI zeros
        self.startServers()

        #Start worker thread running
        threading.Thread(target = self._worker, daemon = True).start()


    def _worker(self):
        print("starting worker thread")
        while True:
            if (self.previewEvent.has_changed()): #a
                self.previewEvent.print()
                self.requestPreview()
            if (self.photoEvent.is_set()): #p
                self.photoEvent.print()
                self.requestPhotos()
                self.photoEvent.clear()
            time.sleep(0.3)

    def requestPreview(self):
        def _requestPreview(self):
            for sock in self.previewsockets:
                SH.sendBytes(sock, "preview".encode(encoding=SH.ENCODETYPE))
            data = [None]*4
            preRes = photo.Photo.PRERES
            cv2.startWindowThread()
            cv2.namedWindow("preview")
            while(self.previewEvent.is_set()):
                for i, sock in enumerate(self.previewsockets):
                   data[i] = SH.receiveBytes(sock)
                viewData = data[self.previewEvent.modifierState -1]
                numdata = numpy.frombuffer(bytes(viewData), dtype=numpy.uint8)
                numdata.shape = (preRes[1], preRes[0], 3)
                cv2.imshow('preview', numdata)
            cv2.destroyAllWindows()
        if self.previewThread is None:
            self.previewThread = threading.Thread(target=_requestPreview, args=[self])
            self.previewThread.start()
        else:
            self.previewEvent.clear()
            self.previewThread.join()
            self.previewThread = None

    def requestPhotos(self):
        def _requestPhotos(self):
            def _receivephoto(self, sock, photoList):
                photoList[self.photosockets.index(sock)] = (SH.receiveBytes(sock))

            print("requesting photos...")
            for sock in self.photosockets:
                SH.sendBytes(sock, "photo".encode(encoding=SH.ENCODETYPE))
            threads = []
            photoList = [None] * 4
            print("photos")
            for sock in self.photosockets:
                writeThread = threading.Thread(target = _receivephoto, args=(self, sock, photoList))
                writeThread.start()
                threads.append(writeThread)
            for thred in threads:
                thred.join()
            print("photos received")
            print("saving photos....")
            gifStitcher.savePhotos(photoList)
        threading.Thread(target = _requestPhotos, args=[self], daemon = True).start()

    def startServers(self):
        command = "python3 -u ~/script/WiggleCam/src/cameraModule.py 2>&1"
        for address in self.SERVERADDRESSES:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(hostname = address)
            self.ssh.append(ssh)
        if self.KILLSCRIPT: 
            self.sendCommandToAllServers("killall -9  python3")
            time.sleep(1)
        self.sendCommandToAllServers(command, self.PRINTREMOTE)
        def _connect (addresses, ports, socketList):
            for i, port in enumerate(ports):
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
                socketList.append(sock)

        _connect(self.SERVERADDRESSES, self.PHOTOPORTS, self.photosockets)
        _connect(self.SERVERADDRESSES, self.PREVIEWPORTS, self.previewsockets)

    def closeServers(self):
        self.sendCommandToAllServers("killall -9  python3")
        for sock in self.previewsockets:
            sock.close()
        for sock in self.photosockets:
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



