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
        self.PHOTOPORT = str(5554 + int(self.ADDRESS[-1:]))
        self.PREVIEWPORT = str(5558 + int(self.ADDRESS[-1:]))
        self.camera = photo.Photo()
        CameraServer.allow_reuse_address = True
        self.photoThread = threading.Thread(target = self._runServer, args = [self.PHOTOPORT, PhotoEventHandler], daemon = True)
        self.previewThread = threading.Thread(target = self._runServer, args = [self.PREVIEWPORT, PreviewEventHandler], daemon = True)
        self.photoThread.start()
        self.previewThread.start()
    
    def _runServer(self, port, eventHandler):
        with CameraServer(('', int(port)), eventHandler, self.camera) as server:
            server.serve_forever()

class CameraServer(socketserver.ThreadingTCPServer):
    def __init__(self, address, handler, camera):
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        socketserver.ThreadingTCPServer.__init__(self, address, handler)
        self.allow_reuse_address = True
        self.camera = camera
        self.isPreviewing = False

class PhotoEventHandler(socketserver.BaseRequestHandler):
    def handle(self):
        requestData = str(SH.receiveBytes(self.request), SH.ENCODETYPE)
        if requestData == "photo":
            photoData = self.server.camera.takePhoto()
            SH.sendBytes(self.request, photoData)

class PreviewEventHandler(socketserver.BaseRequestHandler):
    def handle(self):
        requestData = str(SH.receiveBytes(self.request), SH.ENCODETYPE)
        if requestData == "preview":
            self.server.isPreviewing = not self.server.isPreviewing
            while (self.server.isPreviewing):
                frameData = self.server.camera.getPreviewData()
                SH.sendBytes(self.request, frameData)
