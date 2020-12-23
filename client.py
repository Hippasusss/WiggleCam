from vidgear.gears import NetGear 
import cv2

class Client:

    client = None

    def __init__():
        client = NetGear(receive_mode = True)

    def runPreviewWindow():
        while True:
            frame = client.recv()
            if frame is None:
                break

            cv2.imshow("output", frame)

    def closePreviewWindow():
        cv2.destroyAllWindows()
        client.close()

    def sendInstruction():
        # tell a server to take a photo

    def startPreview(camNumber):
        # start a preview stream with one of the server cams

    def takePhoto():
        # tell all four cameras to take a photo at the same time

