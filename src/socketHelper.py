import sys
import socket

class SH:
    REQUESTSIZE = 28
    ENCODETYPE = "utf-8"
    PADCHAR = '\x00'
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
            data = inputb.to_bytes((inputb.bit_length()//8)+1, 'little')
            typedata = 'i'
        return data + bytes((SH.REQUESTSIZE - 2) - len(data)) + bytes(SH.PINUM, SH.ENCODETYPE) + bytes(typedata, SH.ENCODETYPE)

    def unpadBytes(inputb):
        inputData = bytearray(inputb)
        typedata = chr(inputData[-1])
        piNum = int(chr(inputData[-2]))
        del inputData[-2:]

        data = None
        if typedata == 's':
            data = str(inputData, SH.ENCODETYPE).strip(SH.PADCHAR)
        if typedata == 'i':
            data = int.from_bytes(inputData, 'little')
        if typedata == 'b':
            data = inputData
        return data

    def sendBytes(sock, data):
        dataSize = len(data)
        sock.sendall(SH.padBytes(dataSize))
        sock.sendall(data)

    def receiveBytes(sock):
        def recvall(sock, num):
            data = bytearray()
            while len(data) < num:
                packet = sock.recv(num - len(data))
                if not packet: 
                    break
                data.extend(packet)
            return data
        dataArray = None
        rawInfo = recvall(sock, SH.REQUESTSIZE)
        dataSize = SH.unpadBytes(rawInfo)
        dataArray = recvall(sock, dataSize)
        return dataArray
