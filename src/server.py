import threading
import socketserver
import os

import preview
import photo

class Server:
    # INPUT EVENTS

    def __init__(self, ADDRESS, PORT):
        self.ADDRESS = ADDRESS
        self.PORT = PORT
        self.previewEvent = inputController.KeyEvent('a', isToggle = True)
        self.photoEvent   = inputController.KeyEvent('p')
        self.photo = photo.Photo()

        self.previewWindow = preview.Preview(receiveMode = False, event = previewEvent)

        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print("starting worker thread")
        with socketserver.TCPServer((self.ADDRESS, self.PORT) PhotoEventHandler) as server:
            server.serve_forever()

class PhotoEventHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Get data
        # self.data = self.request.recv(1024).strip()

        # Take Photo and format data
        request = self.request.recv(1024).strip()

        if request is "photo":
            photoPath = self.photo.takePhoto()
            photoSize = os.path.getsize(photoPath)

            # get name and size
            self.reqest.send(f"{photoPath}:{photoSize}".encode())

            with open(filename, "rb") as f:
                while True:
                    block = f.read(1024)
                    if not block:
                        break
                    self.request.sendall(block)

            
            
        


