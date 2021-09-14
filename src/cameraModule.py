import server
import socket
import time

ID = int(socket.gethostname()[-1:])
CLIENTADDRESS = '172.19.181.254'
SERVERADDRESS = socket.gethostname()
PREVIEWPORT = str(5554 + ID)

print("serverStarting")
serverR = server.Server(SERVERADDRESS, PREVIEWPORT)

while True:
    time.sleep(1)


