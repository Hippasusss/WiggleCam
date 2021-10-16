
import os
from picamera import PiCamera

class Photo:

    pathToPhoto = 'currentPhoto.png'
    scriptPath = ''

    def __init__(self):
        self.scriptPath = os.path.dirname(os.path.realpath(__file__))

    def takePhoto(self):
        camera = PiCamera(sensor_mode=2)
        camera.iso=800
        camera.vflip = True
        finalPath = os.path.join(self.scriptPath, self.pathToPhoto)
        camera.capture(finalPath)
        camera.close()
        return finalPath
