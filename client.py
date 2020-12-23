from vidgear.gears import NetGear 
import cv2

class Client:

    SERVERADRESSES = { "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4"}
    PORT = "8000"

    client = None

    def runPreviewWindow(piNumber):
        sendInstruction("preview", piNumber)
        client = NetGear(receive_mode = True, adress = SERVERADRESSES[piNumber], port = PORT)

        while True:
            frame = client.recv()
            if frame is None:
                break

            cv2.imshow("output", frame)

        closePreviewWindow()

    def closePreviewWindow():
        cv2.destroyAllWindows()
        client.close()

    # Sends an instruciton to the desired pi and waits for a response to confime recipt of message
    def sendInstruction(instruction, piNumber):

        if instruction is "preview":
            #send the preview instruction to the pi

        if instruction is "stop":
            # stop the preview window on the pi
        # tell a server to take a photo

        if instruction is "photo":
            # tell the server to stop everythin and take a photo at a set time

