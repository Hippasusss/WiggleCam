from vidgear.gears import NetGear
from vidgear.gears import PiGear

import timer
from inputController import KeyEvent

import cv2

class Preview:


    def __init__(self, receiveMode, event):
        self.resolution = (640, 480)
        self.videoServer = None
        self.receiveMode = receiveMode
        self.previewEvent = event
        self.isPreviewing = False

    def startPreview(self, IP, PORTS, RESOLUTION = (640, 480)):
        self.isPreviewing = True
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
        PORTLOW = 5559
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

            state = int(self.previewEvent.modifierState) - 1
            if state == 4:
                if changeTimer.check():
                    while True:
                        currentIndex+=modifier
                        numCameras = len(frameArray)
                        if (currentIndex <= 0 or currentIndex >= (numCameras - 1)):
                            currentIndex = max(min(currentIndex, numCameras - 1), 0)
                            modifier = -modifier
                        if frameArray[currentIndex] is not None:
                            break
                    changeTimer.reset(timerGap)
            else:
                currentIndex = state

            frame = frameArray[currentIndex]
            if frame is not None:
                cv2.imshow("WiggleCam", frame)

        self.videoServer.close()
        cv2.destroyAllWindows()

    def _previewSend(self):
        self.isPreviewing = True
        options = {"vflip": True,
                   "hflip": True,
                   "exposure_mode": "auto", 
                   "iso": 800, 
                   "exposure_compensation": 15, 
                   "awb_mode": "horizon", 
                   "sensor_mode": 2,
                   }

        self.videoStream = PiGear(resolution = self.resolution, framerate = 13, logging = True, **options).start()

        while self.isPreviewing:
            frame = self.videoStream.read()
            if frame is not None:
                self.videoServer.send(frame)

        self.videoStream.stop()


