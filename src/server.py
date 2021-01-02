from vidgear.gears import NetGear 
from vidgear.gears import PiGear
import threading
import time
import preview

# CAMERA MODULE

# TODO:
# Create seperate threads for:
#
#       - monitoring messages from client 
#       - preview window monitoring 
#       - taking and sending photos
#
# (maybe only need monitoring thread and just have the other two on the main thread)


class Server:

    previewWindow = preview.Preview(receiveMode = False)


