
import os
from picamera import PiCamera

class Photo:

    pathToPhoto = 'currentPhoto.jpg'
    scriptPath = ''

    def __init__(self):
        self.camera = PiCamera()
        self.scriptPath = os.path.dirname(os.path.realpath(__file__))

    def takePhoto(self):
        self.camera.capture(self.pathToPhoto)
        return os.path.join(self.scriptPath, self.pathToPhoto)
