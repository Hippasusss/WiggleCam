import sys

class SH:
    REQUESTSIZE = 128 
    ENCODETYPE = "utf-8"
    PADCHAR = '\x00'
    #CLIENTIP = "172.19.180.254"
    CLIENTIP = "192.168.0.30"
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
        return data + bytes((SH.REQUESTSIZE - 1) - len(data)) + bytes(typedata, SH.ENCODETYPE)

    def unpadBytes(inputb):
        inputData = bytearray(inputb)
        typedata = str(inputData[-1:], SH.ENCODETYPE)
        del inputData[-1:]
        data = None
        if typedata == 's':
            data = str(inputData, SH.ENCODETYPE).strip(SH.PADCHAR)
        if typedata == 'i':
            data = int.from_bytes(inputData, 'little')
        if typedata == 'b':
            data = inputData
        print(typedata)
        return data
