import client 
import time

"""
SERVERADRESSES = [ "172.19.181.1", "172.19.181.2", "172.19.181.3", "172.19.181.4" ]
"""

clientR = client.Client(ADDRESS)

while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        clientR.closeServers()
        print("interrupted: exit succesfull")
        break

