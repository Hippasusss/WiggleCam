import client 
import time

"""
SERVERADRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
"""

ADDRESS = "172.19.181.254"
PREVIEWPORTS = ("5555", "5556", "5557", "5558")

clientR = client.Client(ADDRESS, PREVIEWPORTS)

while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        clientR.closeServers()
        print("interrupted")
        break

