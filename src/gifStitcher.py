from pathlib import Path
import imageio
import numpy
import PIL
import os
from datetime import datetime

def savePhotos(listOfPhotos):
    filetype = ".png"
    now=datetime.now().strftime("%d-%m-%y %H%M%S")
    path = f"{str(Path.home())}/photos/{now}"
    images = []

    # save photos as png images
    for i, photo in enumerate(listOfPhotos):
        filePath = f"{path}/IMG{i+1} {now}{filetype}"
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        size = len(photo)
        image = PIL.Image.frombytes('RGB', (4064, 3040), bytes(photo))
        images.append(image)
        image.save(filePath)
        print(f"saved at: {filePath}")

    # save images as a wiggle video 
    numPhotos = len(listOfPhotos)
    numLoops = 5
    print(f"numPhotos = {numPhotos}")
    arrangement = []
    for j in range(numLoops):
        for i in range((numPhotos * 2) - 2):
            currentPhoto = abs(numPhotos - (i+1))
            print(f"added: {currentPhoto}")
            arrangement.append(images[currentPhoto])
    writer = imageio.get_writer(f"{path}/VID {now}.mp4", fps = 6)

    for image in arrangement:
        writer.append_data(numpy.array(image))
    writer.close()


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


