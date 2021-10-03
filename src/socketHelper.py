class SH:
    REQUESTSIZE = 128 
    ENCODETYPE = "utf-8"
    PADCHAR = '\x00'
    def padBytes(inputb):
        data = bytes(inputb, SH.ENCODETYPE)
        return data + bytes(SH.REQUESTSIZE - len(data))

    def unpadBytes(inputb):
        return str(inputb, SH.ENCODETYPE).strip(SH.PADCHAR)
