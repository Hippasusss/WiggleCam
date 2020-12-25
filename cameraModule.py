import server
import time

CLIENTADRESS = "172.19.181.254"
# CLIENTADRESS = "172.19.180.254"
# CLIENTADRESS = "192.168.1.86"
# CLIENTADRESS = "192.168.1.86"
PREVIEWPORT = "5454"

module = server.Server()

module.previewWindow.startPreview(CLENTADRESS, PREVIEWPORT)

module.previewWindow.waitForTermination()






