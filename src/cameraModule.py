import server
import socket
import time

"""
CLIENTADRESS = "172.19.181.254"
CLIENTADRESS = "172.19.180.254"
CLIENTADRESS = "192.168.1.86"
"""


ID = int(socket.gethostname()[-1:])

print(ID)

CLIENTADRESS = "172.19.181.254"
PREVIEWPORT = str(5554 + ID)

print(PREVIEWPORT)
RESOLUTION = (640, 480)

module = server.Server()

module.previewWindow.startPreview(CLIENTADRESS, PREVIEWPORT, RESOLUTION );

module.previewWindow.waitForTermination()






