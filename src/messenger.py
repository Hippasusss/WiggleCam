import threading
import time
import socket

class Messenger:

    def __init__(self, address, ports, isSender):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(ip, port)
        self.sock.listen(5)

        self.isSender = isSender
        return
        
    def startMessenger(self):
        routine = self._messageSender if self.isSender else self._messageReceiver
        thread = threading.Thread(target = self._messenger, daemon = True)
        thread.start()
        return

    def _messageSender(self);
        while True:
            #do your bits please

    def _messageReceiver(self);
        while True:
            #do your bits please
        
