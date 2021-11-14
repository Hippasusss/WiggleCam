import server
import time

print("serverStarting")
serverR = server.Server()

serverR.photoThread.join()
serverR.previewThread.join()


