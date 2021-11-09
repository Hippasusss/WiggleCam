from pathlib import Path
import imageio
import PIL
import os
from datetime import datetime

def savePhotos(listOfPhotos):
    path = f"{str(Path.home())}/photos"
    filetype = ".png"
    now=datetime.now().strftime("%d-%m-%y %H%M%S")
    for i, photo in enumerate(listOfPhotos):
        filePath = f"{path}/{now}/IMG{i+1} {now}{filetype}"
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        size = len(photo)
        image = PIL.Image.frombytes('RGB', (4064, 3040), bytes(photo))
        image.save(filePath)

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


