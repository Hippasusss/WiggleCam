class SH:
    REQUESTSIZE = 128 
    ENCODETYPE = "utf-8"
    PADCHAR = '\x00'
    #CLIENTIP = "172.19.180.254"
    CLIENTIP = "192.168.0.30"
    def padBytes(inputb):
        data = bytes(inputb, SH.ENCODETYPE)
        return data + bytes(SH.REQUESTSIZE - len(data))

    def unpadBytes(inputb):
        return str(inputb, SH.ENCODETYPE).strip(SH.PADCHAR)
