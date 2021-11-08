import io
import os
import sys 
import picamera
import imageio
import PIL

class Photo:
    PRERES = (320,240)
    PHORES = (4064, 3040)

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

    def savePhotos(listOfPhotos):
        path = f"{str(Path.home())}/photos"
        filetype = ".png"
        now=datetime.now().strftime("%d-%m-%y %H%M%S")
        for i, photo in enumerate(photoList):
            filePath = f"{path}/{now}/IMG{i+1} {now}{filetype}"
            os.makedirs(os.path.dirname(filePath), exist_ok=True)
            size = len(photo)
            image = PIL.Image.frombytes('RGB', size, photo)
            image.save(filepath)
                #WRITE FILE

    def stitch(listOfPhotos, name):
        images = []
        for photo in listOfPhotos:
            images.append(imageio.imread(photo, as_gray=False, pilmode="RGB"))
        numPhotos = len(listOfPhotos)
        numLoops = 5
        print(f"numPhotos = {numPhotos}")
        arrangement = []
        for j in range(numLoops):
            print(f"loop: {j}")
            for i in range((numPhotos * 2) - 2):
                currentPhoto = abs(numPhotos - (i+1))
                print(f"photo:{currentPhoto}")
                arrangement.append(images[currentPhoto])
        writer = imageio.get_writer("test.mp4", fps = 6)

        for im in arrangement:
            writer.append_data(im)
        writer.close()



