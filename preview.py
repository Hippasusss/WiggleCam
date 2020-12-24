from vidgear.gears import NetGear 
from vidgear.gears import PiGear 
import threading
import cv2

class Preview:

    videoServer = None
    previewThread = None
    preiviewing = False 
    receive = None

    def __init__(receiveMode):
        receive = receiveMode


    def startPreview(self, IP, PORT):
        self.previewing = True
        routine = None
        if self.receive:
            routine = self._previewReceive
        else:
            routine = self._previewSend


        if self.previewThread is None:
            print("connecting to IP: {0}".format(IP))
            print("connecting on PORT: {0}".format(PORT))
            self.videoServer = NetGear(receive_mode = self.receive, adress = IP,  port = PORT)
            self.previewThread = threading.Thread(target = routine)
            self.previewThread.start()
            print("Started preview")


    def stopPreview(self):
        self.previewing = False
        if self.previewThread is not None:
            self.videoServer.close()
            cv2.destroyAllWindows()
            self.previewThread.join()

    def waitForTermination(self);
        self.previewThread.join()

    def _previewReceive(self):
        print("Success!")

        while self.previewing:
            frame = self.videoServer.recv()
            if frame is None:
                break

            cv2.imshow("output", frame)

        self.stopPreview()

    def _previewSend(self)

        options = {"hflip": True, 
                        "exposure_mode": "auto", 
                        "iso": 800, 
                        "exposure_compensation": 15, 
                        "awb_mode": "horizon", 
                        "sensor_mode": 0}

        self.videoStream = PiGear(resolution = (640, 480), framerate = 24, logging = True, **options).start()

        while self.previewing:
            frame = self.videoStream.read()

            if frame is None:
                break

            self.videoServer.send(frame)

        self.videoStream.stop()
        self.stopPreview()


