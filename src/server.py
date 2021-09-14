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


        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print(f"starting worker thread: {self.PORT}")
        with PhotoServer(('', int(self.PORT)), PhotoEventHandler) as server:
            print(f"Connecting on ADDRESS:{self.ADDRESS}, PORT{self.PORT}")
            server.serve_forever()

class PhotoServer(socketserver.TCPServer):
    def service_actions(self):
        print("server Running")
        self.handle_request()
        time.sleep(0.2)


class PhotoEventHandler(socketserver.BaseRequestHandler):

    photo = photo.Photo()
    previewWindow = preview.Preview(receiveMode = False, event = None)

    def handle(self):
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

        if request is "preview":
            if previewWindow.isPreviewing is False:
                previewWindow.startPreview()
            else:
                preiviewWindow.stopPreview()
            
        


