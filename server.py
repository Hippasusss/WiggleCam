from vidgear.gears import NetGear 
from vidgear.gears import PiGear
import threading
import time

# CAMERA MODULE

# TODO:
# Create seperate threads for:
#
#       - monitoring messages from client 
#       - preview window monitoring 
#       - taking and sending photos
#
# (maybe only need monitoring thread and just have the other two on the main thread)

# MAINCOMP   = "192.168.1.120"
# CONTROLLER = "192.168.1.86"
CLIENTADRESS = "192.168.1.160"
PREVIEWPORT = "8000"

class Server:
    options = None
    videoServer = None
    videoStream = None
    videoStreaming = False

    monitorThread = None
    previewThread = None

    previewing = False
    monitoring = False

    def __init__(self):
        self.options = {"hflip": True, 
                        "exposure_mode": "auto", 
                        "iso": 800, 
                        "exposure_compensation": 15, 
                        "awb_mode": "horizon", 
                        "sensor_mode": 0}




    def startPreview(self):

        self.previewing = True
        if self.previewThread is None:
            self.videoServer = NetGear(adress = CLIENTADRESS, port = PORT)
            self.previewThread = threading.Thread(target=self.preview)
            self.previewThread.start()
            print ("Started preview stream")



    def stopPreview(self):

        self.previewing =
        if self.previewThread is not None:
            self.previewThread.join()
            self.videoStream.stop()
            self.videoServer.close()
            print("Stopped preview stream")

    def preview(self):
        self.videoStream = PiGear(resolution = (640, 480), framerate = 24, logging = True, **self.options).start()

        while self.previewing:
            frame = self.videoStream.read()

            if frame is None:
                break

            self.videoServer.send(frame)



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

