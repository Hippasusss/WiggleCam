import client 
import time

#SERVERADRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
PREVIEWPORT = "5454"
ADRESS = "172.19.181.254"

controller = client.Client()

controller.previewWindow.startPreview(ADRESS, PREVIEWPORT)

controller.previewWindow.waitForTermination()


