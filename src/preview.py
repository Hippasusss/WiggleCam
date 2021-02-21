from vidgear.gears import NetGear
from vidgear.gears import PiGear
import threading
import cv2
from imutils import build_montages

class Preview:
    videoServer = None
    previewThread = None
    isPreviewing = False
    receive = None
    resolution = (640, 480)


    def __init__(self, receiveMode):
        self.receive = receiveMode


    def startPreview(self, IP, PORTS, RESOLUTION = (640, 480)):
        
        options = {"multiserver_mode": True}

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
            print("connecting on PORTS: {0}".format(PORTS))
            self.videoServer = NetGear(receive_mode = True, pattern = 1, address = IP,  port = PORTS, protocol = "tcp", **options)

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
        cv2.startWindowThread()
        cv2.namedWindow("output")
        frameDict = {}

        while self.isPreviewing:
            data = self.videoServer.recv()
            unique_address, frame = data

            if frame is None:
                break

            (h, w) = frame.shape[:2]

            # update the extracted frame in the received frame dictionary
            frameDict[unique_address] = frame

            # build a montage using data dictionary
            montages = build_montages(frameDict.values(), (w, h), (2, 1))

            # display the montage(s) on the screen
            for (i, montage) in enumerate(montages):

                cv2.imshow("Montage Footage {}".format(i), montage)
                cv2.imshow("output", frame)

        self.stopPreview()

    def _previewSend(self):
        print("Started preveiew thread")

        options = {"hflip": True,
                   "exposure_mode": "auto", 
                   "iso": 800, 
                   "exposure_compensation": 15, 
                   "awb_mode": "horizon", 
                   "sensor_mode": 0,
                   "multiserver_mode": True}

        self.videoStream = PiGear(resolution = self.resolution, framerate = 24, logging = True, **options).start()

        while self.isPreviewing:
            frame = self.videoStream.read()

            if frame is None:
                break

            self.videoServer.send(frame)

        self.videoStream.stop()
        self.stopPreview()

