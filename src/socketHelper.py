
class SH:
    REQUESTSIZE = 64
    def padBytes(inputb, length = 64):
        return inputb + bytes(length- len(inputb))
