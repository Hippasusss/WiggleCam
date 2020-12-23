from vidgear.gears import NetGear 
from vidgear.gears import PiGear


class Server:

    CLIENTADRESS = "192.168.1.160"
    PORT = "8000"

    options = None
    server = None
    stream = None
    streaming = False

    def __init__():

        # add various Picamera tweak parameters to dictionary
        self.options = {"hflip": True, 
                   "exposure_mode": "auto", 
                   "iso": 800, 
                   "exposure_compensation": 15, 
                   "awb_mode": "horizon", 
                   "sensor_mode": 0}

        self.server = NetGear(adress = CLIENTADRESS, port = PORT)


    def runPreview():
        streaming = True

        # open pi video stream with defined parameters
        self.stream = PiGear(resolution = (640, 480), framerate = 24, logging = True, **options).start()

        while streaming:
            frame = stream.read()

            if frame is None:
                break

            self.server.send(frame)


    def endPreview():
        streaming = False
        self.stream.close()
        self.server.close()


    def takePhoto():
        # Take a photo


    def sendData():
        # send the photo that was taken to the client  


    def sendDataStream():
        frame = self.stream.read()
        self.server.send(frame)
        # send formatted data
        # formatting data will be the job of the camera script, this is
        # just a generic clent server;











