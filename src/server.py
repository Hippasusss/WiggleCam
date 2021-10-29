import threading
import socketserver
import socket
import os
import time
import io

import photo
from socketHelper import SH

class Server:
    # INPUT EVENTS
    def __init__(self):
        self.ADDRESS = socket.gethostname() 
        self.ID = int(self.ADDRESS[-1:])
        self.PORT = str(5554 + self.ID) 

        print(f"starting worker thread: {self.PORT}")
        PhotoServer.allow_reuse_address = True
        with PhotoServer(('', int(self.PORT)), PhotoEventHandler) as server:
            print(f"Connecting on ADDRESS:{self.ADDRESS}, PORT:{self.PORT}")
            server.serve_forever()

class PhotoServer(socketserver.ThreadingTCPServer):
    def __init__(self, address, handler ):
        self.camera = photo.Photo()
        self.photoEvent = threading.Event()
        self.isPreviewing = False

        self.allow_reuse_address = True
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        socketserver.ThreadingTCPServer.__init__(self, address, handler)

    def service_actions(self):
        print("Waiting for next request")
        self.handle_request()

class PhotoEventHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request = SH.unpadBytes(self.request.recv(SH.REQUESTSIZE))
        if request == "prev":
            self.server.isPreviewing = not self.server.isPreviewing
            while (self.server.isPreviewing):
                while (self.server.photoEvent.is_Set() == False): #untill photo request
                    frameData = self.server.camera.getPreviewData()
                    self.sendBytes(frameData)
                self.sendBytes(self.server.camera.takePhoto())
                self.server.photoEvent.clear()
        elif request == "phot":
            if(self.server.isPreviewing)
                self.server.photoEvent.set()
            else:
                photoData = self.server.camera.takePhoto()
                self.sendBytes(photoData)

    def sendBytes(self, data):
        dataSize = len(data)
        self.request.sendall(SH.padBytes(dataSize))
        self.request.sendall(data)
