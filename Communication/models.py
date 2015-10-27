from django.db import models
from incident.models import Incident
import facebook
# Create your models here.
class SocialMediaReport(models.Model):
    incident = models.ForeignKey(Incident)
    timestamp = models.DateTimeField('time published')
    socialMediaText = models.TextField()


class MediaPublisherLoader:
    @staticmethod
    def load_publisher(type):
        module_name = "Communication.models"
        module = __import__(module_name, fromlist=[''])
        publisher_class = getattr(module, type)
        publisher = publisher_class()
        return publisher

class MediaPublisher:
    def compose_and_publish(self,message):
        pass

class FacebookPublisher(MediaPublisher):

    def compose_and_publish(self,message):
        cfg = {
        "page_id"      : "1153212874703747",
        "access_token" : "CAALFYDni6RUBAMXDuqZChNozy0eYcZBdsZA9e9hUKJgThZBGSqLGci4HS13SQyp989TIlrkbpVjblxew0PLG0W4tu7w8mldfWEFZCXEw9fIm9xzXME0fzdW6JyzI06Xbiw4ZCd6iI1BeLMcFPCiHbjmt3gS8ISuxGHX0m1rbzMDm3HofamZAmpvefSC6DVtM0EZD"   # Step 3
        }
        try:
            api = self.get_api(cfg)
            msg = "This message is converted from Message object: " + message
            status = api.put_wall_post(msg)
        except Exception as e:
            return e.__str__()
        return 'Sucessfully posted status, please check!'

    def get_api(self, cfg):
        graph = facebook.GraphAPI(cfg['access_token'])
        # Get page token to post as the page. You can skip
        # the following if you want to post as yourself.
        resp = graph.get_object('me/accounts')
        page_access_token = None
        for page in resp['data']:
            if page['id'] == cfg['page_id']:
                page_access_token = page['access_token']
        graph = facebook.GraphAPI(page_access_token)
        return graph
    # You can also skip the above if you get a page token:
    # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
    # and make that long-lived token as in Step 3


