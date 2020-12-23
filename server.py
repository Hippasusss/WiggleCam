from vidgear.gears import VideoGear
from vidgear.gears import NetGear 
from vidgear.gears import PiGear


class server:

    def __init__():

        # add various Picamera tweak parameters to dictionary
        self.options = {"hflip": True, 
                   "exposure_mode": "auto", 
                   "iso": 800, 
                   "exposure_compensation": 15, 
                   "awb_mode": "horizon", 
                   "sensor_mode": 0}

        # open pi video stream with defined parameters
        self.stream = PiGear(resolution = (640, 480), framerate = 60, logging = True, **options).start()

    def startPreview():
        # shot this sensor on the preview screen

    def takePhoto():
        # take a photo at a specific time and prepare it to be sent over network

    def sendData():
        # send the photo that was taken to the ser

    def sendDataStream():
        # send formatted data
        # formatting data will be the job of the camera script, this is
        # just a generic clent server;











# import libraries
from vidgear.gears import NetGear
import cv2

#define netgear client with `receive_mode = True` and default settings
client = NetGear(receive_mode = True)

# infinite loop
while True:
    # receive frames from network
    frame = client.recv()

    # check if frame is None
    if frame is None:
        #if True break the infinite loop
        break

    # do something with frame here

    # Show output window
    cv2.imshow("Output Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        #if 'q' key-pressed break out
        break

# close output window
cv2.destroyAllWindows()
# safely close client
client.close()
