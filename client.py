from vidgear.gears import NetGear 
import cv2

#CONTROLLER
SERVERADRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
PORT = "8000"

class Client:


    client = None

    def startPreviewWindow(self, piNumber):
        piNumber -= 1
        #sendInstruction("preview", piNumber)

        print("connecting to IP: {0}".format(SERVERADRESSES[piNumber]))
        print("connecting on PORTP: {0}".format(PORT))

        self.client = NetGear(receive_mode = True, adress = SERVERADRESSES[piNumber], port = PORT)

        print("Success!")

        while True:
            frame = self.client.recv()
            if frame is None:
                break

            cv2.imshow("output", frame)

        closePreviewWindow()

    def closePreviewWindow(self):
        cv2.destroyAllWindows()
        client.close()

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

