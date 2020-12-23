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

class Server:

    CLIENTADRESS = "192.168.1.160"
    PORT = "8000"

    options = None
    server = None
    stream = None
    streaming = False

    def __init__():

        threading.Thread(target=messageMonitor)
        thread.start()


        self.options = {"hflip": True, 
                   "exposure_mode": "auto", 
                   "iso": 800, 
                   "exposure_compensation": 15, 
                   "awb_mode": "horizon", 
                   "sensor_mode": 0}

        self.server = NetGear(adress = CLIENTADRESS, port = PORT)


    def runPreview():
        streaming = True

        self.stream = PiGear(resolution = (640, 480), framerate = 24, logging = True, **options).start()
        print("Created Stream...")

        while streaming:
            frame = stream.read()

            if frame is None:
                break

            self.server.send(frame)


    def endPreview():
        streaming = False
        self.stream.close()
        self.server.close()
        print("Closed Stream...")


    # takes a photo and sends it back to the client 
    def takePhoto():
        print("Took Photo...")


    def messageMonitor():
        print("Started monitoring for messages...")
        while True:
            # do stuff

        print("Stopped monitoring for messages")









