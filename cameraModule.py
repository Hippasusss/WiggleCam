import server
import time

# MAINCOMP   = "192.168.1.160"
# CONTROLLER = "192.168.1.86"
CLIENTADRESS = "192.168.1.86"
PREVIEWPORT = "8000"

module = server.Server()

module.previewWindow.startPreview("127.0.0.1", PREVIEWPORT)

module.previewWindow.waitForTermination()






