import threading
import socketserver
import socket
import os
import time

import preview
import photo
from socketHelper import SH

class Server:
    # INPUT EVENTS

    def __init__(self):
        self.ADDRESS = socket.gethostname() 
        self.ID = int(self.ADDRESS[-1:])
        self.PORT = str(5554 + self.ID) 

        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print(f"starting worker thread: {self.PORT}")
        PhotoServer.allow_reuse_address = True
        with PhotoServer(('', int(self.PORT)), PhotoEventHandler, self.ADDRESS, self.PORT) as server:
            print(f"Connecting on ADDRESS:{self.ADDRESS}, PORT:{self.PORT}")
            server.serve_forever()

class PhotoServer(socketserver.ThreadingTCPServer):
    def __init__(self, address, handler, host, port):
        self.HOST = host
        self.PORT = port 
        self.allow_reuse_address = True
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        socketserver.ThreadingTCPServer.__init__(self, address, handler)
    def service_actions(self):
        print("Waiting for next request")
        self.handle_request()

class PhotoEventHandler(socketserver.BaseRequestHandler):
    photo = photo.Photo()
    previewWindow = preview.Preview(receiveMode = False, event = None)
    def handle(self):
        # Take Photo and format data
        request = self.request.recv(SH.REQUESTSIZE)
        request = SH.unpadBytes(request)

        if request == "photo":
            photoPath = self.photo.takePhoto()
            photoSize = os.path.getsize(photoPath)
            name, extension = photoPath.split(".")
            name = name + socket.gethostname()[-1] + "." + extension
        
            nameSize = SH.padBytes(f"{name}:{photoSize}")
            self.request.sendall(nameSize)

            with open(photoPath, "rb") as f:
                block = f.read(photoSize)
                if not block:
                   return 
                self.request.sendall(bytes(block))
            #self.removeAllPhotos()

        elif request == "preview":
            print("previewing")
            if PhotoEventHandler.previewWindow.isPreviewing is False:
                #self.previewWindow.startPreview(self.server.HOST, str(int(self.server.PORT) + 4))
                try:
                    PhotoEventHandler.previewWindow.startPreview(SH.CLIENTIP, str(int(self.server.PORT) + 4))
                except:
                    pass
            else:
                PhotoEventHandler.preiviewWindow.stopPreview()
        
        else:
            print("Incorrect Request")
            self.request.sendall(SH.padBytes("incorrect"))
            
        print("Request Handled")

    def removeAllPhotos(self):
        print("Removing Photos")
        extension = [".jpg", ".gif", ".png", ".raw"]
        directory = os.path.dirname(os.path.realpath(__file__)) 
        files = os.listdir(directory)
        for item in files:
            for e in extension:
                if item.endswith(e):
                    os.remove(os.path.join(directory, item))
        print("Photos Removed")
