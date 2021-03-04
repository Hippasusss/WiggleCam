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

    # INPUT EVENTS
    previewEvent = inputController.KeyEvent('a', isToggle = True)
    photoEvent   = inputController.KeyEvent('p')

    previewWindow = preview.Preview(receiveMode = False, event = previewEvent)

    def __init__(self, ADDRESS, PORT):
        self.ADDRESS = ADDRESS
        self.PORT = PORT

        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print("starting worker thread")
        while True:
            time.sleep(0.3)
            print("worker idle...")
