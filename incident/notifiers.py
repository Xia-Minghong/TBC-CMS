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


    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def unregister_all(self):
        if self.observers:
            del self.observers[:]

    def notify(self, object, message, *args, **kwargs):
        print("==========" + str(self) + " is notifying " + str(len(self.observers)) + " observers=========")
        for observer in self.observers:
            observer.update(notifier=self, object=object, message=message, *args, **kwargs)
            print("==========" + str(self) + " notified " + str(observer) + "=========")

    def get_objects(self):
        pass



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

    def get_objects(self):
        return Incident.objects.exclude(status = 'closed')

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

    def get_objects(self):
        return InciUpdate.objects.all()

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

    def get_objects(self):
        return Dispatch.objects.all()

    def recent_dispatches(self, timedelta):
        import datetime
        now = datetime.datetime.now()
        cut_off = now - timedelta
        dispatches = Dispatch.objects.filter(time__gte=cut_off)
        serializer = DispatchSerializer(dispatches, many=True)
        return serializer.data

    def propose_dispatch(self, incident):
        agency = Agency.objects.order_by('?')[0]
        resource = ""
        if incident.type == 'accident':
            resource = "Police"
        elif incident.type == 'fire':
            resource = "Fire Engine, Emergency Ambulance"
        elif incident.type == 'riot':
            resource = "Rescue and Evacuation "
        elif incident.type == 'gas_leak':
            resource = "Gas Leak Control"

        from django.utils import timezone
        dispatch = Dispatch(incident = incident, agency = agency, resource = resource, time = timezone.now())
        dispatch.save()
        self.notify(dispatch,"propose_dispatch")
