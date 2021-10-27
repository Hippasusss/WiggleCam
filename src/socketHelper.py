import sys
import socket

class SH:
    REQUESTSIZE = 28 
    ENCODETYPE = "utf-8"
    PADCHAR = '\x00'
    #CLIENTIP = "172.19.180.254"
    PHOTOREQUEST = 1
    PREVIEWREQUEST = 2
    PINUM = socket.gethostname()[-1:]
    def padBytes(inputb):
        data = None 
        typedata = None
        if isinstance(inputb, bytes):
            data = inputb
            typedata = 'b'
        if isinstance(inputb, str):
            data = bytes(inputb, SH.ENCODETYPE)
            typedata = 's'
        if isinstance(inputb, int):
            data = inputb.to_bytes(sys.getsizeof(data), 'little')
            typedata = 'i'
        return data + bytes((SH.REQUESTSIZE - 2) - len(data)) + bytes(SH.PINUM, SH.ENCODETYPE) + bytes(typedata, SH.ENCODETYPE)

    def unpadBytes(inputb):
        inputData = bytearray(inputb)
        typedata = chr(inputData[-1])
        piNum = chr(inputData[-2])
        del inputData[-2:]

        data = None
        if typedata == 's':
            data = str(inputData, SH.ENCODETYPE).strip(SH.PADCHAR)
        if typedata == 'i':
            data = int.from_bytes(inputData, 'little')
        if typedata == 'b':
            data = inputData
        return data
