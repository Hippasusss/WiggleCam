
import threading
import time
import socket
import paramiko
import cv2
import numpy

from socketHelper import SH
import gifStitcher
import photo

class Client:
    SERVERADDRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
    KILLSCRIPT = False
    PRINTREMOTE = False

    def __init__(self):
        self.ADDRESS = "172.19.181.254"
        self.PORTS = ("5555", "5556", "5557", "5558")
        self.PREVIEWPORTS = ("5559", "5560", "5561", "5562")
        self.ssh = []
        self.sockets = []
        self.debugThreads = []


        # Start the scripts running on the PI zeros
        self.startServers()
        # Create the socket connections to the PI Zeros
        self.connectToServers()

        #Start worker thread running
        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print("starting worker thread")
        while True:
            time.sleep(0.3)

    def requestPreview(self):
        self.sendRequestToAllServers("preview")
        data = []*4
        preRes = photo.Photo.PRERES
        cv2.startWindowThread()
        cv2.namedWindow("preview")
        while(self.previewEvent.is_set()):
            for i, sock in enumerate(self.sockets):
               data[i] = SH.receiveBytes(sock)
            viewData = data[self.previewEvent.modifierState -1]
            numdata = numpy.frombuffer(bytes(viewData), dtype=numpy.uint8)
            numdata.shape = (preRes[1], preRes[0], 3)
            cv2.imshow('preview', numdata)
        cv2.destroyAllWindows()

    def requestPhotos(self):
        def _receivephoto(self, sock, photoList):
            photoList[self.sockets.index(sock)] = (SH.receiveBytes(sock))
        self.sendRequestToAllServers("photo")
        threads = []
        photoList = [None] * 4
        for sock in self.sockets:
            writeThread = threading.Thread(target = _receivephoto, args=(self, sock, photoList))
            writeThread.start()
            threads.append(writeThread)
        for thred in threads:
            thred.join()

        gifStitcher.savePhotos(photoList)

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



