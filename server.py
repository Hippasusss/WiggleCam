from vidgear.gears import NetGear 
from vidgear.gears import PiGear
import threading

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

class videoServer:

    CLIENTADRESS = "192.168.1.160"
    PORT = "8000"

    options = None
    videoServer = None
    videoStream = None
    videoStreaming = False

    def __init__():

        threading.Thread(target=messageMonitor)
        thread.start()


        self.options = {"hflip": True, 
                   "exposure_mode": "auto", 
                   "iso": 800, 
                   "exposure_compensation": 15, 
                   "awb_mode": "horizon", 
                   "sensor_mode": 0}

        self.videoServer = NetGear(adress = CLIENTADRESS, port = PORT)


    def runPreview():
        videoStreaming = True

        self.videoStream = PiGear(resolution = (640, 480), framerate = 24, logging = True, **options).start()
        print("Created videoStream...")

        while videoStreaming:
            frame = videoStream.read()

            if frame is None:
                break

            self.videoServer.send(frame)


    def endPreview():
        videoStreaming = False
        self.videoStream.close()
        self.videoServer.close()
        print("Closed videoStream...")


    # takes a photo and sends it back to the client 
    def takePhoto():
        print("Took Photo...")


    def messageMonitor():
        print("Started monitoring for messages...")
        while True:
            # do stuff

        print("Stopped monitoring for messages")









