import io
import os
import sys 
import picamera

class Photo:
    PRERES = (320,240)
    PHORES = (4056, 3040)

    def __init__(self):
        self.camera = picamera.PiCamera(sensor_mode = 2)
        self.mode = 0
        self.camera.resolution = Photo.PRERES

    def takePhoto(self):
        self.setSettings("photo")
        data = self._getCameraData()
        self.setSettings("preview")
        return data 
    
    def getPreviewData(self):
        data = self._getCameraData(True)
        return data

    def _getCameraData(self, video=False):
        data = io.BytesIO()
        self.camera.capture(data, use_video_port=video, format='rgb')
        data.seek(0)
        dataArray = data.read()
        data.close()
        print(sys.getsizeof(dataArray))
        return dataArray

    def setSettings(self, mode):
        if (mode == "photo"):
            self.camera.vflip = True
            self.camera.exposure_mode = "auto"
            self.camera.iso = 800
            self.camera.exposure_compensation = 15
            self.camera.awb_mode = "horizon"
            self.camera.resolution = Photo.PHORES
        if (mode == "preview"):
            self.camera.resolution = Photo.PRERES




