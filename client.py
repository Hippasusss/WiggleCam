
from vidgear.gears import VideoGear
from vidgear.gears import PiGear 
from vidgear.gears import NetGear 

class client:
    def __init__():
        #init

    def receiveData():
        # receive data

    def sendInstruction():
        # tell a server to take a photo

    def startPreview(camNumber):
        # start a preview stream with one of the server cams

    def takePhoto():
        # tell all four cameras to take a photo at the same time













# shit from internet to refrence

stream = VideoGear(source='test.mp4').start() #Open any video stream
server = NetGear() #Define netgear server with default settings

# infinite loop until [Ctrl+C] is pressed
while True:
    try: 
        frame = stream.read()
        # read frames

        # check if frame is None
        if frame is None:
            #if True break the infinite loop
            break

        # do something with frame here

        # send frame to server
        server.send(frame)

    except KeyboardInterrupt:
        #break the infinite loop
        break

# safely close video stream
stream.stop()
# safely close server
writer.close()
