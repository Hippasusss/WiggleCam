import threading
import preview

import photo

class Server:
    # INPUT EVENTS

    def __init__(self, ADDRESS, PORT):
        self.ADDRESS = ADDRESS
        self.PORT = PORT
        self.previewEvent = inputController.KeyEvent('a', isToggle = True)
        self.photoEvent   = inputController.KeyEvent('p')

        self.previewWindow = preview.Preview(receiveMode = False, event = previewEvent)

        workerThread = threading.Thread(target = self._worker, daemon = True)
        workerThread.start()

    def _worker(self):
        print("starting worker thread")
        while True:
            time.sleep(0.3)
            print("worker idle...")
