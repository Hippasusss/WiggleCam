import client 
import time

SERVERADRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
PREVIEWPORT = "8000"

controller = client.Client()

controller.previewWindow.startPreview(SERVERADRESSES[1], PREVIEWPORT)

controller.waitForTermination()


