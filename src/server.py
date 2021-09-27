import threading
import socketserver
import socket
import os
import time

import preview
import photo

class Server:
    # INPUT EVENTS

    def __init__(self, ADDRESS, PORT):
        self.ADDRESS = ADDRESS
        self.PORT = PORT


        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print(f"starting worker thread: {self.PORT}")
        with PhotoServer(('', int(self.PORT)), PhotoEventHandler) as server:
            print(f"Connecting on ADDRESS:{self.ADDRESS}, PORT{self.PORT}")
            server.serve_forever()

class PhotoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def service_actions(self):
        print("server Running")
        self.handle_request()
        time.sleep(0.2)


class PhotoEventHandler(socketserver.BaseRequestHandler):

    photo = photo.Photo()
    previewWindow = preview.Preview(receiveMode = False, event = None)
    encodeType = "utf-8"

    def handle(self):
        # Take Photo and format data
        request = str(self.request.recv(1024).strip(), self.encodeType)
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
                while True:
                    block = f.read(photoSize)
                    if not block:
                        break
                    self.request.sendall(bytes(block))
        elif request == "preview":
            if previewWindow.isPreviewing is False:
                previewWindow.startPreview()
            else:
                preiviewWindow.stopPreview()
        else:
            print("Incorrect Request")
            self.request.sendall(bytes("incorrect", self.encodeType))
            
        


