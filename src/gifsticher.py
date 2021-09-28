
import imageio

class GifStitcher():
    
    FRAMEDURATION = 0.2
    GIF DURATION = 15
    
    def stitchGif(listOfPhotos):
        images = []
        numPhotos = len(listOfPhotos)
        for i in range((numPhotos * 2) - 2):
            currentPhoto = i - (i % numPhotos)
            images.append(listOfPhotos[currentPhoto])
        imagio.mimsave('newGif.gif', images, fps=4)


