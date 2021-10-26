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
    camera = photo.Photo()
    def handle(self):
        # Take Photo and format data
        request = SH.unpadBytes(self.request.recv(SH.REQUESTSIZE))

        if request == "prev":
            while (True): #untill photo request
                frameData = self.camera.getPreviewData()
                self.sendBytes(frameData)

        if request == "phot":
            photoData = self.camera.takePhoto()
            self.sendBytes(photoData)
        
        else:
            print("Incorrect Request")
            self.request.sendall(SH.padBytes("incorrect"))
            
        print("Request Handled")

    def sendBytes(self, data):
        dataSize = len(data)
        self.request.sendall(SH.padBytes(dataSize))
        self.request.sendall(data)
'''
    def sendBytes(self, datai):
        with io.BytesIO() as data:
            data.write(datai)
            data.seek(0)
            dataSize = int(data.getbuffer().nbytes)
            self.request.sendall(SH.padBytes(dataSize))
            block = data.read(dataSize)
            self.request.sendall(block)
'''
