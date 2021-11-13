from pathlib import Path
from datetime import datetime

import numpy
import os
import cv2

def savePhotos(listOfPhotos):
    imageType = ".jpg"
    videoType = ".mp4"
    now = datetime.now().strftime("%d-%m-%y %H%M%S")
    path = f"{str(Path.home())}/photos/{now}"
    images = []
    imageSize = (4064, 3040)

    # save photos as png images
    for i, photo in enumerate(listOfPhotos):
        filePath = f"{path}/IMG{i+1} {now}{imageType}"
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        numdata = numpy.frombuffer(bytes(photo), dtype=numpy.uint8)
        numdata.shape = (imageSize[1], imageSize[0], 3)
        images.append(numdata)
        cv2.imwrite(filePath, numdata)
        print(f"saved at: {filePath}")

    ## save images as a wiggle video 
    numPhotos = len(listOfPhotos)
    numLoops = 5
    arrangement = []
    # save the order of the images into an array
    codec = cv2.VideoWriter_fourcc(*'H264')
    video = cv2.VideoWriter(f"{path}/VID {now}{videoType}", codec, 6, imageSize)
    for j in range(numLoops):
        for i in range((numPhotos * 2) - 2):
            currentPhotoIndex = abs(numPhotos - (i+1))
            video.write(images[currentPhotoIndex])
    video.release()


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


