import pymongo


class DatabaseService:
    def __init__(self, host, port, database):
        self.__host = host
        self.__port = port
        self.__database = database
        self.__client = self.__tryToConnect()

    def __tryToConnect(self):
        try:
            clientz = pymongo.MongoClient("mongodb://" + self.__host + ":" + str(self.__port) + "/")
            return clientz
        except Exception:
            print("Server not available")
            return None

    def getClient(self):
        return self.__client

    def getDatabase(self):
        return self.__client[self.__database]
