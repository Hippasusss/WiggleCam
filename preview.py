from vidgear.gears import NetGear
from vidgear.gears import PiGear
import threading
import cv2

class Preview:
    videoServer = None
    previewThread = None
    isPreviewing = False
    receive = None
    resolution = (640, 480)

    def __init__(self, receiveMode):
        self.receive = receiveMode


    def startPreview(self, IP, PORT, RESOLUTION = (640, 480)):
        self.isPreviewing = True
        routine = None
        if self.receive:
            print("Receiving")
            routine = self._previewReceive
        else:
            print("Sending")
            routine = self._previewSend
            self.resolution = RESOLUTION


        if self.previewThread is None:
            print("connecting to IP: {0}".format(IP))
            print("connecting on PORT: {0}".format(PORT))
            self.videoServer = NetGear(receive_mode = self.receive, address = IP,  port = PORT, protocol = "tcp")
            self.previewThread = threading.Thread(target = routine)
            self.previewThread.start()


    def stopPreview(self):
        self.isPreviewing = False
        if self.previewThread is not None:
            self.videoServer.close()
            cv2.destroyAllWindows()

    def waitForTermination(self):
        self.previewThread.join()

    def _previewReceive(self):
        print("Started preveiew thread")

        while self.isPreviewing:
            frame = self.videoServer.recv()
            if frame is None:
                break
            cv2.imshow("output", frame)

        self.stopPreview()

    def _previewSend(self):
        print("Started preveiew thread")

        options = {"hflip": True, 
                        "exposure_mode": "auto", 
                        "iso": 800, 
                        "exposure_compensation": 15, 
                        "awb_mode": "horizon", 
                        "sensor_mode": 0}

        self.videoStream = PiGear(resolution = self.resolution, framerate = 24, logging = True, **options).start()

        while self.isPreviewing:
            frame = self.videoStream.read()

            if frame is None:
                break

            self.videoServer.send(frame)

        self.videoStream.stop()
        self.stopPreview()


