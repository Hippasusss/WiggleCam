import server
import socket
import time

"""
CLIENTADRESS = "172.19.181.254"
CLIENTADRESS = "172.19.180.254"
CLIENTADRESS = "192.168.1.86"
"""

IPEND = int((socket.gethostbyname(socket.gethostname()).split(",")[3])
CLIENTADRESS = "172.19.181.254"
PREVIEWPORT = str(5554 + IPEND)
RESOLUTION = (640, 480)

module = server.Server()

module.previewWindow.startPreview(CLIENTADRESS, PREVIEWPORT, RESOLUTION );

module.previewWindow.waitForTermination()






