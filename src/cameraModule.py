import server
import socket
import time

ID = int(socket.gethostname()[-1:])
CLIENTADDRESS = "172.19.181.254"
PREVIEWPORT = str(5554 + ID)

serverR = server.Server.Client(CLIENTADDRESS, PREVIEWPORT)







