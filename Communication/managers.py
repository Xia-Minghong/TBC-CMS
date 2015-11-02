__author__ = 'Jiaxiang'

from incident.observers import AbstractObserver
from incident.notifiers import *
from.media_publishers import MediaPublisherLoader




class SocialMediaReportMgr(AbstractObserver):
    _instance = None

    #overwriting the existing __new__() method
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SocialMediaReportMgr, cls).__new__(
                                cls, *args, **kwargs)

            #Registering interest
            IncidentMgr().register(cls._instance)
            InciUpdateMgr().register(cls._instance)
            DispatchMgr().register(cls._instance)
        return cls._instance

    def update(self, notifier, object, *args, **kwargs):
        print("\n================" + str(self) + "is notified by " + str(notifier) + "================\n")

#####Instantiate SocialMediaReportMgr right away
SocialMediaReportMgr()



class ReportMgr:


    def generate_message(self):
        import time
        from incident.views import RECENT_INTERVAL
        #localtime = time.asctime( time.localtime(time.time()) )
        #localtime = timezone.localtime(timezone.now())
        incidents_data = IncidentMgr().recent_incidents(RECENT_INTERVAL)
        updates_data = InciUpdateMgr().recent_updates(RECENT_INTERVAL)
        dispatches_data = DispatchMgr().recent_dispatches(RECENT_INTERVAL)
        message = 'The testing is successful!!!\nTime tested: ' + time.ctime()

        message += ("\n\nRecent Incidents\n====================")
        for incident in incidents_data:
            message += ("\n")
            message += ("\nIncident   : " + incident["name"])
            message += ("\ntype       : " + incident["type"])
            message += ("\nStatus     : " + incident["status"])
            message += ("\nSeverity   : " + str(incident["severity"]))
            message += ("\nTime       : " + incident["time"])
            message += ("\nLocation   : " + incident["location"])
            message += ("\nDescription: " + incident["description"])
            message += ("\n")

        message += ("\n\nRecent Updates\n====================")
        for update in updates_data:
            message += ("\n")
            message += ("\nIncident        : " + update["incident"]["name"])
            message += ("\nUpdatd by       : " + update["agency"]["name"])
            message += ("\nStatus          : " + ("approved","pending")[update["is_approved"]])
            message += ("\nUpdated Severity: " + str(update["updated_severity"]))
            message += ("\nDescription     : " + update["description"])
            message += ("\n")

        message += ("\n\nRecent Dispatches\n====================")
        for dispatch in dispatches_data:
            message += ("\n")
            message += ("\nIncident         : " + dispatch["incident"]["name"])
            message += ("\nDispatched Agency: " + dispatch["agency"]["name"])
            message += ("\nResource         : " + dispatch["resource"])
            message += ("\nTime             : " + incident["time"])
            message += ("\n")
        return message

    def publish(self, type):
        message = self.generate_message()
        publisher = MediaPublisherLoader.load_publisher(type=type)
        return publisher.compose_and_publish(message)


    TIME_INTERVAL = 10

    def periodically_publish(self,type):
        import time, threading
        threading.Timer(self.TIME_INTERVAL, lambda:self.periodically_publish(type)).start()
        message = self.publish(type)
        print("**********************\n" + time.ctime() + '\n' + message + "\n*********************")

class DispatchSmsMgr(AbstractObserver):

    _instance = None

    #overwriting the existing __new__() method
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DispatchSmsMgr, cls).__new__(
                                cls, *args, **kwargs)

            #Registering interest
            DispatchMgr().register(cls._instance)
        return cls._instance

    def update(self, notifier, object, *args, **kwargs):
        if isinstance(notifier, DispatchMgr):
            dispatch = object
            self.publish(dispatch, type="SmsPublisher")
        print("\n================" + str(self) + "is notified by " + str(notifier) + "================\n")

    def generate_message(self, dispatch):
        incident = dispatch.incident
        agency = dispatch.agency
        content = \
            """
Dear {}:

    An incident, {}, happened at {} at {}. Below is a short descrition of the incident.

    Description: {}

    As such, {}

    Thank you!

Best regards,
CMS Team""" \
            .format(agency.name, incident.name, incident.time, incident.location, incident.description, dispatch.resource)
        return content

    def publish(self, dispatch, type="SmsPublisher"):
        message = self.generate_message(dispatch)
        publisher = MediaPublisherLoader.load_publisher(type)
        return publisher.compose_and_publish(message=message, recipient_list=[dispatch.agency.contact,])

#####Instantiate SocialMediaReportMgr right away
DispatchSmsMgr()