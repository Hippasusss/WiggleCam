import client
import inputController
import time
import warnings
warnings.filterwarnings("ignore")

clientR = client.Client()
inputControl = inputController.Input()
inputControl.addEvent(inputController.KeyEvent('a', clientR.requestPreview, isToggle = True, modifiers = ["1", "2", "3", "4", "5"]))

inputControl.addEvent(inputController.KeyEvent('p', clientR.requestPhotos))
while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        clientR.closeServers()
        print("interrupted: exit succesfull")
        break

from subprocess import call
call(["stty", "sane"])

