import threading
import time

class Messager:

    monitorThread = None
    monitoring = False

    def startMessageMonitor(self):

        self.monitoring = True
        if self.monitorThread is None:
            self.monitorThread = threading.Thread(target=self.messageMonitor)
            self.monitorThread.start()

        print("Started monitoring for messages...")

    def stopMessageMonitor(self):
        self.monitoring = False
        if self.monitorThread is not None:
            self.monitorThread.join()
            self.monitorThread = None

        print("Stopped Monitoring for messages...")

    def messageMonitor(self):
        while self.monitoring:
            time.sleep(0.1)
            print("monitoring")

    def sendMessage(self, instruction):

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

    def sendFile(self, file):
        # send file

