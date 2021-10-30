import threading
import socketserver
import socket
import os
import time
import io

import photo
from socketHelper import SH

class Server:
    def __init__(self):
        self.ADDRESS = socket.gethostname() 
        self.PORT = str(5554 + int(self.ADDRESS[-1:]) 
        PhotoServer.allow_reuse_address = True
        with PhotoServer(('', int(self.PORT)), PhotoEventHandler) as server:
            server.serve_forever()

class PhotoServer(socketserver.ThreadingTCPServer):
    def __init__(self, address, handler ):
        socketserver.ThreadingTCPServer.__init__(self, address, handler)
        self.camera = photo.Photo()
        self.photoEvent = threading.Event()
        self.isPreviewing = False

class PhotoEventHandler(socketserver.BaseRequestHandler):
    def handle(self):
        requestData = SH.receiveBytes(self.request)
        if requestData == "prev":
            self.server.isPreviewing = not self.server.isPreviewing
            while (self.server.isPreviewing):
                while (self.server.photoEvent.is_Set() == False): #untill photo request
                    frameData = self.server.camera.getPreviewData()
                    SH.sendBytes(sock, frameData)
                self.sendBytes(self.server.camera.takePhoto())
                self.server.photoEvent.clear()
        elif requestData == "phot":
            if(self.server.isPreviewing)
                self.server.photoEvent.set()
            else:
                photoData = self.server.camera.takePhoto()
                SH.sendBytes(sock, photoData)

