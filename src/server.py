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
        self.PORT = str(5554 + int(self.ADDRESS[-1:]))
        PhotoServer.allow_reuse_address = True
        with PhotoServer(('', int(self.PORT)), PhotoEventHandler) as server:
            server.serve_forever()

class PhotoServer(socketserver.ThreadingTCPServer):
    def __init__(self, address, handler ):
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        socketserver.ThreadingTCPServer.__init__(self, address, handler)
        self.allow_reuse_address = True
        self.camera = photo.Photo()
        self.photoEvent = threading.Event()
        self.isPreviewing = False

class PhotoEventHandler(socketserver.BaseRequestHandler):
    def handle(self):
        requestData = str(SH.receiveBytes(self.request), SH.ENCODETYPE)
        if requestData == "preview":
            self.server.isPreviewing = not self.server.isPreviewing
            while (self.server.isPreviewing):
                while (self.server.photoEvent.is_set() == False): #untill photo request
                    frameData = self.server.camera.getPreviewData()
                    SH.sendBytes(self.request, frameData)
                self.sendBytes(self.server.camera.takePhoto())
                self.server.photoEvent.clear()
        elif requestData == "photo":
            if(self.server.isPreviewing):
                self.server.photoEvent.set()
            else:
                photoData = self.server.camera.takePhoto()
                SH.sendBytes(self.request, photoData)

