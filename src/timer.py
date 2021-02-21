import time

class Timer:
    startTime = 0
    resetTime = 0

    def start(self, resetTime):
        self.startTime = time.time()
        self.resetTime = resetTime

    def check(self):
        currentTime = time.time()
        reset = (currentTime - self.startTime) > self.resetTime
        return reset

