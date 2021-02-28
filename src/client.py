from vidgear.gears import NetGear 
import cv2
import preview
import inputController

#CONTROLLER

# client side controller of everything 
class Client:

    PORT = None
    ADDRESS = None

    previewWindow = preview.Preview(receiveMode = True)
    inputControl = inputController.Input()

    running = True

    def __init__(ADDRESS, PORT):
        self.ADDRESS = ADRESS
        self.PORT = PORT
        inputControl.startChecking()

    def startClient():
        while(running):

    def endClient():
        running = False
        




