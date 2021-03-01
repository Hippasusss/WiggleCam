from vidgear.gears import NetGear
from vidgear.gears import PiGear

import timer
from inputController import KeyEvent

import cv2

class Preview:
    previewEvent = None
    videoServer = None
    receiveMode = None
    resolution = (640, 480)


    def __init__(self, receiveMode, event):
        self.receiveMode = receiveMode
        self.previewEvent = event


    def startPreview(self, IP, PORTS, RESOLUTION = (640, 480)):
        self.resolution = RESOLUTION
        options = {"multiserver_mode": True}
        routine = self._previewReceive if self.receiveMode else self._previewSend 
        self.videoServer = NetGear(receive_mode = self.receiveMode, 
                                   pattern = 1, 
                                   address = IP,  
                                   port = PORTS, 
                                   protocol = "tcp", 
                                   **options)

        routine()

    def stopPreview(self):
        self.isPreviewing = False
        if self.videoServer is not None: 
            self.videoServer.close()
        cv2.destroyAllWindows()

    def _previewReceive(self):
        PORTLOW = 5555
        cv2.startWindowThread()
        cv2.namedWindow("WiggleCam")

        timerGap = 0.1
        changeTimer = timer.Timer()
        changeTimer.reset(timerGap)

        frameArray = [None] * 4
        currentIndex = 0
        modifier = 1

        while self.previewEvent.is_set():
            data = self.videoServer.recv()
            if data is None:
                break
            senderPort, frame = data
            writeFrameIndex = int(senderPort) - PORTLOW
            frameArray[writeFrameIndex] = frame
            if changeTimer.check():
                while True:
                    currentIndex+=modifier
                    if (currentIndex == 0 or currentIndex == (len(frameArray) - 1)):
                        modifier = -modifier
                    if frameArray[currentIndex] is not None:
                        break
                changeTimer.reset(timerGap)
            frame = frameArray[currentIndex]
            if frame is not None:
                cv2.imshow("WiggleCam", frame)

        self.videoServer.close()
        cv2.destroyAllWindows()

    def _previewSend(self):
        options = {"hflip": True,
                   "exposure_mode": "auto", 
                   "iso": 800, 
                   "exposure_compensation": 15, 
                   "awb_mode": "horizon", 
                   "sensor_mode": 0,
                   }

        self.videoStream = PiGear(resolution = self.resolution, framerate = 24, logging = True, **options).start()

        while self.previewEvent.is_set():
            frame = self.videoStream.read()
            if frame is not None:
                self.videoServer.send(frame)

        self.videoStream.stop()


