
import imageio


FRAMEDURATION = 0.2
GIFDURATION = 15

def stitch(listOfPhotos, name):
    images = []
    for photo in listOfPhotos:
        images.append(imageio.imread(photo))
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
    imageio.mimsave(f'{name}.gif', arrangement, fps=6)


