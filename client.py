from vidgear.gears import NetGear 
import threading
import cv2
import preview

#CONTROLLER

class Client:

    previewWindow = preview.Preview(receiveMode = True)

    # Sends an instruciton to the desired pi and waits for a response to confime recipt of message
    def sendInstruction(self, instruction, piNumber):

        if instruction is "preview":
            hello=True
            #send the preview instruction to the pi

        if instruction is "stop":
            hello=True
            # stop the preview window on the pi
        # tell a server to take a photo

        if instruction is "photo":
            hello=True
            # tell the server to stop everythin and take a photo at a set time


