import client 
import time

"""

SERVERADRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
ADRESS = "172.19.181.1"
ADRESS = "172.19.180.254"
ADRESS = "192.168.1.86"
ADRESS = "172.19.181.254"

"""

ADRESS = "172.19.181.254"
PREVIEWPORT = "5555"


controller = client.Client()

controller.previewWindow.startPreview(ADRESS, PREVIEWPORT )

print("wait")
controller.previewWindow.waitForTermination()


