import client 
import time

"""
SERVERADRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
"""

ADDRESS = "172.19.181.254"
PREVIEWPORTS = ("5555", "5556", "5557", "5558")


controller = client.Client()

controller.previewWindow.startPreview(ADDRESS, PREVIEWPORTS)

print("wait")
controller.previewWindow.waitForTermination()


