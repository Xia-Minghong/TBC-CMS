__author__ = 'Jiaxiang'

from abc import ABCMeta, abstractmethod
from .notifiers import *

class AbstractObserver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class EmergencyManagerMgr(AbstractObserver):
    _instance = None

    #overwriting the existing __new__() method
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EmergencyManagerMgr, cls).__new__(
                                cls, *args, **kwargs)

            #Registering interest
            IncidentMgr().register(cls._instance)
            InciUpdateMgr().register(cls._instance)
            DispatchMgr().register(cls._instance)
        return cls._instance

    def update(self, *args, **kwargs):
        notifier = kwargs["notifier"]
        print("\n\n=====================")
        type(notifier)
        print("args= ")
        for arg in args:
            print(arg)
        print()
        print("kwargs= " + str(kwargs["notifier"]) + kwargs["apple"])
        print("=====================\n\n")

    # def __str__(self):
    #     return "I'm an instance of EmergencyManagerMgr"