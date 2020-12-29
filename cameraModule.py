import server
import time

"""
CLIENTADRESS = "172.19.181.254"
CLIENTADRESS = "172.19.180.254"
CLIENTADRESS = "192.168.1.86"
"""

CLIENTADRESS = "172.19.181.254"
PREVIEWPORT = "5555"

module = server.Server()

module.previewWindow.startPreview(CLIENTADRESS, PREVIEWPORT, RESOLUTION = (640, 480))

module.previewWindow.waitForTermination()






