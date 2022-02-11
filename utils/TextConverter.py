class TextConverter:

    @staticmethod
    def encodeString(string:str):
        return string.encode('utf-8')

    @staticmethod
    def decodeBytes(bytes:bytes):
        return bytes.decode('utf-8')
