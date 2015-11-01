__author__ = 'Jiaxiang'

from abc import ABCMeta, abstractmethod
from .notifiers import *

class AbstractObserver(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def update(self, notifier, object, *args, **kwargs):
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

    def update(self, notifier, object, *args, **kwargs):
        '''
        Please add in what happens after the system notified EmergencyManagerMgr something changed
        '''


#####Instantiate EmergencyManagerMgr right away
EmergencyManagerMgr()


class SystemMonitor(AbstractObserver):
    _instance = None

    #overwriting the existing __new__() method
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SystemMonitor, cls).__new__(
                                cls, *args, **kwargs)

            #Registering interest
            IncidentMgr().register(cls._instance)
            InciUpdateMgr().register(cls._instance)
            DispatchMgr().register(cls._instance)
        return cls._instance

    def update(self, notifier, object, *args, **kwargs):
        print("\n================" + str(self) + "is notified by " + str(notifier) + "================\n")

#####Instantiate EmergencyManagerMgr right away
SystemMonitor()




