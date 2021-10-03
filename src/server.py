import threading
import socketserver
import socket
import os
import time

import preview
import photo
import socketHelper

class Server:
    # INPUT EVENTS

    def __init__(self, ADDRESS, PORT):
        self.ADDRESS = ADDRESS
        self.PORT = PORT


        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print(f"starting worker thread: {self.PORT}")
        with PhotoServer(('', int(self.PORT)), PhotoEventHandler, self.ADDRESS, self.PORT) as server:
            print(f"Connecting on ADDRESS:{self.ADDRESS}, PORT:{self.PORT}")
            server.serve_forever()

class PhotoServer(socketserver.ThreadingTCPServer):
    def __init__(self, adress, handler, host, port):
        socketserver.ThreadingTCPServer.__init__(self, adress, handler)
        self.HOST = host
        self.PORT = port 

    def service_actions(self):
        self.removeAllPhotos()
        self.handle_request()
        print("Request Handled")

    def removeAllPhotos(self):
        extension = [".jpg", ".gif", ".png", ".raw"]
        directory = os.path.dirname(os.path.realpath(__file__)) 
        
        files = os.listdir(directory)

        for item in files:
            for e in extension:
                if item.endswith(e):
                    os.remove(os.path.join(directory, item))


class PhotoEventHandler(socketserver.BaseRequestHandler):

    photo = photo.Photo()
    previewWindow = preview.Preview(receiveMode = False, event = None)
    encodeType = "utf-8"

    def handle(self):
        # Take Photo and format data
        request = str(self.request.recv(SH.REQUESTSIZE).strip(), self.encodeType)
        print(request)

        if request == "photo":
            photoPath = self.photo.takePhoto()
            photoSize = os.path.getsize(photoPath)
            name, extension = photoPath.split(".")
            finalName = name + socket.gethostname()[-1] + "." + extension

            # send name and filesize to client
            nameSize = bytes(f"{finalName}:{photoSize}", self.encodeType)
            print(nameSize)
            self.request.sendall(nameSize)

            with open(photoPath, "rb") as f:
                block = f.read(photoSize)
                if not block:
                   return 
                self.request.sendall(bytes(block))


        elif request == "preview":
            print("previewing")
            if self.previewWindow.isPreviewing is False:
                self.previewWindow.startPreview(self.server.HOST, self.server.PORT)
            else:
                self.preiviewWindow.stopPreview()
        else:
            print("Incorrect Request")
            self.request.sendall(bytes("incorrect", self.encodeType))
            
        


