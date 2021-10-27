import client 
import time
import warnings
warnings.filterwarnings("ignore")

clientR = client.Client()

while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        clientR.closeServers()
        print("interrupted: exit succesfull")
        break

from subprocess import call
call(["stty", "sane"])

