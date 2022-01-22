class User:
    def __init__(self, id, name, lastname, age, train_data):
        self.__id = id
        self.__name = name
        self.__lasname = lastname
        self.__age = age
        self.__train_data = train_data

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getLastname(self):
        return self.__lasname

    def getAge(self):
        return self.__age

    def getTrainData(self):
        return self.__train_data
