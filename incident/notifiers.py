__author__ = 'Jiaxiang'

from .models import *
from .serializers import *

class AbstractNotifier(object):
    def __init__(self):
        pass

    def register(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
            print("==========" + str(observer) + "is registerd at" + str(self) + "=========")
            print("==========" + str(len(self.observers)) + " observers have now registered at" + str(self) + "=======")
        else:
            print("=========lololololol, fail==========")


    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def unregister_all(self):
        if self.observers:
            del self.observers[:]

    def notify(self, *args, **kwargs):
        print("==========" + str(self) + " is notifying " + str(len(self.observers)) + " observers=========")
        for observer in self.observers:
            observer.update(*args, notifier=self, **kwargs)
            print("==========" + str(self) + " notified " + str(observer) + "=========")



class IncidentMgr(AbstractNotifier):
    _instance = None

    def __construct(self):
        self.observers = []

    #overwriting the existing __new__() method
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(IncidentMgr, cls).__new__(
                                cls, *args, **kwargs)
            print("========================creating instance===================")
            cls._instance.__construct()
        return cls._instance

    def recent_incidents(self, timedelta):
        import datetime
        now = datetime.datetime.now()
        cut_off = now - timedelta
        incidents = Incident.objects.filter(time__gte=cut_off)
        serializer = IncidentSerializer(incidents, many=True)
        return serializer.data

class InciUpdateMgr(AbstractNotifier):
    _instance = None

    def __construct(self):
        self.observers = []

    #overwriting the existing __new__() method
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(InciUpdateMgr, cls).__new__(
                                cls, *args, **kwargs)
            cls._instance.__construct()
        return cls._instance

    def recent_updates(self, timedelta):
        import datetime
        now = datetime.datetime.now()
        cut_off = now - timedelta
        inci_updates = InciUpdate.objects.filter(time__gte=cut_off)
        serializer = InciUpdateSerializer(inci_updates, many=True)
        return serializer.data

class DispatchMgr(AbstractNotifier):
    _instance = None

    def __construct(self):
        self.observers = []

    #overwriting the existing __new__() method
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DispatchMgr, cls).__new__(
                                cls, *args, **kwargs)
            cls._instance.__construct()
        return cls._instance

    def recent_dispatches(self, timedelta):
        import datetime
        now = datetime.datetime.now()
        cut_off = now - timedelta
        dispatches = Dispatch.objects.filter(time__gte=cut_off)
        serializer = DispatchSerializer(dispatches, many=True)
        return serializer.data
