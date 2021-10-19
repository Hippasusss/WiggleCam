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

    def handle(self):
        # Take Photo and format data
        request = SH.unpadBytes(self.request.recv(SH.REQUESTSIZE))
        if request == "preview":
            while (True): #untill photo request
                frameData = photo.getPreviewData()
                frameSize = photoData.getbuffer().nbytes
                while(True): #untill frame sent
                    block = frameData.read(1024)
                    if not block:

                        frameData.seek(0)
                        return 
                    self.request.sendall(bytes(block))


        if request == "photo":
            photoData = self.photo.takePhoto()
            photoSize = photoData.getbuffer().nbytes
            name = socket.gethostname()[-1] 
        
            nameSize = SH.padBytes(f"{name}:{photoSize}")
            self.request.sendall(nameSize)

            while(True):
                block = photoData.read(4096)
                if not block:
                   return 
                self.request.sendall(bytes(block))
            #self.removeAllPhotos()
        
        else:
            print("Incorrect Request")
            self.request.sendall(SH.padBytes("incorrect"))
            
        print("Request Handled")

