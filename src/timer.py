
import time

class Timer:

    startTime
    resetTime;

    def startTimer(self, resetTime):
        self.startTime = time.time()
        self.startTime = resetTime

    def checkTimer(self, autoReset):
        currentTime = time.time()
        reset = (currentTime - self.startTime) > self.resetTime
        if(reset) self.startTime = currentTime

        return reset

