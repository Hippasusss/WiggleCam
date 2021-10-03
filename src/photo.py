
import os
from picamera import PiCamera

class Photo:

    pathToPhoto = 'currentPhoto.jpg'
    scriptPath = ''

    def __init__(self):
        self.scriptPath = os.path.dirname(os.path.realpath(__file__))

    def takePhoto(self):
        camera = PiCamera()
        camera.capture(self.pathToPhoto)
        camera.close()
        return os.path.join(self.scriptPath, self.pathToPhoto)
