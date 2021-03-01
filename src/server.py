import threading
import preview

# CAMERA MODULE

# TODO:
# Create seperate threads for:
#
#       - monitoring messages from client 
#       - preview window monitoring 
#       - taking and sending photos
#
# (maybe only need monitoring thread and just have the other two on the main thread)


class Server:

    PORT = None
    ADDRESS = None

    previewWindow = preview.Preview(receiveMode = True, event = previewEvent)
    workerThread = threading.thread(target = _worker, daemon = True)

    previewEvent = inputController.KeyEvent()
    photoEvent = inputController.KeyEvent()

    def __init__(self, ADDRESS, PORT):
        self.ADDRESS = ADRESS
        self.PORT = PORT
        inputControl.startChecking()

    def startClient(self):
        workerThread.start()

    def _worker(self):
        while True:
            if previewEvent.is_set():
                previewWindow.startPreview(ADDRESS, PORT)
            else:
                previewWindow.stopPreview()
