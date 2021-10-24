
import io
import os
import picamera

class Photo:

    def __init__(self):
        self.camera = picamera.PiCamera(sensor_mode = 2)
        self.mode = 0
        self.resolution = (4056, 3040)
        self.previewStream = io.BytesIO()

    def takePhoto(self):
        self.setSettings("photo")
        stream = io.BytesIO()
        self.camera.capture(stream, format="rgb")
        self.setSettings("preview")
        return stream 
    
    def getPreviewData(self):
        self.previewStream.seek(0)
        self.camera.capture(self.previewStream, use_video_port=True, format='jpg')
        self.previewStream.seek(0)
        return self.previewStream

    def setSettings(self, mode):
        if (mode == "photo"):
            self.camera.vflip = True
            self.camera.exposure_mode = "auto"
            self.camera.iso = 800
            self.camera.exposure_compensation = 15
            self.camera.awb_mode = "horizon"
            self.camera.resolution = (4056, 3040)
        if (mode == "preview"):
            self.camera.resolution = (320,280)


