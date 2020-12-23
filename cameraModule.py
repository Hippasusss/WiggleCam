import server
import time

module = server.Server()

module.startMessageMonitor()

print("main sleep")
time.sleep(3)
print("main up")

module.stopMessageMonitor()

time.sleep(1)

module.startMessageMonitor()

print("main sleep")
time.sleep(3)
print("main up")

module.stopMessageMonitor()



print("main end")

