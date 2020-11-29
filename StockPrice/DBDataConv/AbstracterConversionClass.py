from abc import ABCMeta, abstractmethod

class AbstracterConversionClass(metaclass=ABCMeta):

    @ abstractmethod
    def DBData_to_List(self,Item):
        pass
