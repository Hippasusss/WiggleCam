import time

class Timer:
    startTime = 0
    resetTime = 0

    def reset(self, timerGap):
        self.startTime = time.time()
        self.resetTime = timerGap

    def check(self):
        currentTime = time.time()
        reset = (currentTime - self.startTime) > self.resetTime
        return reset

