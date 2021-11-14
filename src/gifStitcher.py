from pathlib import Path
from datetime import datetime

import threading
import numpy
import os
import cv2

def savePhotos(listOfPhotos):
    photoThread = threading.Thread(target = _savePhotos, args=[listOfPhotos])
    photoThread.start()

def _savePhotos(listOfPhotos):
    imageType = ".png"
    videoType = ".mp4"
    now = datetime.now().strftime("%d-%m-%y %H%M%S")
    path = f"{str(Path.home())}/photos/{now}"
    images = []
    imageSize = (4064, 3040)

    ## save photos as png images ---------

    for i, photo in enumerate(listOfPhotos):
        filePath = f"{path}/IMG{i+1} {now}{imageType}"
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        numdata = numpy.frombuffer(bytes(photo), dtype=numpy.uint8)
        numdata.shape = (imageSize[1], imageSize[0], 3)
        images.append(numdata)
        cv2.imwrite(filePath, numdata)
        print(f"photo saved at: {filePath}")

    ## save images as a wiggle video -----

    # downres images
    for image in images:
        image = cv2.resize(image, None, fx = 0.2, fy = 0.2)

    # save
    numPhotos = len(listOfPhotos)
    numLoops = 5
    videoPath = f"{path}/VID {now}{videoType}"
    arrangement = []
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(videoPath, codec, 6, (images[0].shape[1], images[0].shape[0]))
    for j in range(numLoops):
        for i in range((numPhotos * 2) - 2):
            currentPhotoIndex = abs(numPhotos - (i+1))
            video.write(images[currentPhotoIndex])
    video.release()
    print(f"video saved at: {videoPath}")
