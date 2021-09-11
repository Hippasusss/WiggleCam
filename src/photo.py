
from picamera import PiCamera

class Photo:

    pathToPhoto = '~/photos/currentPhoto.jpg'

    def __init__(self):
        self.camera = PiCamera()

    def takePhoto(self):
        self.camera.capture(pathToPhoto)
        return pathToPhoto
