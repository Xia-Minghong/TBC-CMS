__author__ = 'Jiaxiang'

from abc import ABCMeta, abstractmethod
from .notifiers import *
from .views import publish


class AbstractObserver(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def update(self, notifier, object, message, *args, **kwargs):
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

    def update(self, notifier, object, message, *args, **kwargs):

        if isinstance(notifier,IncidentMgr) and message=="create":
            incidents = notifier.get_objects()
            serializer = IncidentSerializer(incidents, many=True)
            publish(serializer, "incidents", request="")
        elif isinstance(notifier,InciUpdateMgr) and message=="create":
            print("*************tetsing*********")
            updates = notifier.get_objects()
            serializer = InciUpdateSerializer(updates, many=True)
            publish(serializer, "inciupdates", request="")
        elif isinstance(notifier, DispatchMgr) and message=="propose_dispatch":
            dispatches = notifier.get_objects()
            serializer = DispatchSerializer(dispatches, many=True)
            publish(serializer, "dispatches", request="")

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

    def update(self, notifier, object, message, *args, **kwargs):
        print("\n================" + str(self) + "is notified by " + str(notifier) + "================\n")
        from .views import publish
        if isinstance(notifier,IncidentMgr) and message=="approve":
            incidents = notifier.get_objects()
            serializer = IncidentSerializer(incidents, many=True)
            publish(serializer, "incidents", request="")

        elif isinstance(notifier,InciUpdateMgr) and (message=="approve" or message=="reject"):
            updates = notifier.get_objects()
            serializer = InciUpdateSerializer(updates, many=True)
            publish(serializer, "updates", request="")

        elif isinstance(notifier,DispatchMgr) and (message=="approve" or message=="reject"):
            dispatches = notifier.get_objects()
            serializer = DispatchSerializer(dispatches, many=True)
            publish(serializer, "dispatches", request="")
        """
        consider moving publishing parts here?
        """

#####Instantiate EmergencyManagerMgr right away
SystemMonitor()




