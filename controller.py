import client 
import time

controller = client.Client()

controller.startPreviewWindow(1)

while True:
    try:
        time.sleep(0.2)
    except KeyboardInterrupt:
        controller.closePreviewWindow()
