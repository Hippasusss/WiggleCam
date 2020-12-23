import server
import time

module = server.Server()

module.startPreview()

print("main sleep")
time.sleep(20)
print("main up")

module.stopPreview()



print("main end")

