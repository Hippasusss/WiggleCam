from vidgear.gears import NetGear 
from vidgear.gears import PiGear
import threading
import time
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

    previewWindow = preview.Preview(receiveMode = False)

    monitorThread = None
    monitoring = False

    def startMessageMonitor(self):

        self.monitoring = True
        if self.monitorThread is None:
            self.monitorThread = threading.Thread(target=self.messageMonitor)
            self.monitorThread.start()

        print("Started monitoring for messages...")

    def stopMessageMonitor(self):
        self.monitoring = False
        if self.monitorThread is not None:
            self.monitorThread.join()
            self.monitorThread = None

        print("Stopped Monitoring for messages...")

    def messageMonitor(self):
        while self.monitoring:
            time.sleep(0.5)
            print("monitoring")


    # takes a photo and sends it back to the client 
    def takePhoto(self):
        print("Took Photo...")

