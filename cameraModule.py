import server
import time

CLIENTADRESS = "172.19.181.254"
# CLIENTADRESS = "172.19.180.254"
# CLIENTADRESS = "192.168.1.86"
# CLIENTADRESS = "192.168.1.86"
PREVIEWPORT = "5454"

module = server.Server()

module.previewWindow.startPreview("127.0.0.1", PREVIEWPORT)

module.previewWindow.waitForTermination()






