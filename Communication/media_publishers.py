__author__ = 'Jiaxiang'
from incident.models import Incident
import facebook
import tweepy
from App import settings


class MediaPublisherLoader:
    @staticmethod
    def load_publisher(type):
        module_name = "Communication.media_publishers"
        module = __import__(module_name, fromlist=[''])
        publisher_class = getattr(module, type)
        publisher = publisher_class()
        return publisher

class MediaPublisher:
    def compose_and_publish(self,message,recipient_list=None):
        pass



class FacebookPublisher(MediaPublisher):

    def compose_and_publish(self,message,recipient_list=None):
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
class EmailPublisher(MediaPublisher):
    def compose_and_publish(self, message = 'Message not passed in',recipient_list=['zhou0235@e.ntu.edu.sg',]): #'hone5com@gmail.com', 'jfu003@e.ntu.edu.sg', 'C130062@e.ntu.edu.sg',
        try:
            from django.core.mail import send_mass_mail
            subject = 'Crisis Report'
            from_email = settings.EMAIL_HOST_USER
            message = (subject, message, from_email, recipient_list)
            send_mass_mail((message,),fail_silently=False, auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD)
        except Exception as e:
            return str(e)
        return_message = 'Email successfully sent to: '
        for recipient in recipient_list:
            return_message += ('\n' + recipient)
        return return_message

class TwitterPublisher(MediaPublisher):
    def compose_and_publish(self,message='Message not passed in',recipient_list=None):
        # Fill in the values noted in previous step here
        cfg = {
            "consumer_key"        : "ylMFOLS6Hj9ecylbJjTWx62jq",
            "consumer_secret"     : "y1vH3n6KIbNDGlfjCnVzja9sXCcRDeFpOfTgNGaBu33uzVRlPp",
            "access_token"        : "4042587680-k8G0OJfwlE9GOq6cI6uXMvRAC7nUCOGaSowyWV8",
            "access_token_secret" : "hNVl76JO9bnDHkR1UPZK1Ypfoh4rIRG95HmA0H319VV2G"
            }
        try:
            api = self.get_api(cfg)
            tweet = message     ##Edit the format here
            status = api.update_status(status=tweet)
            # Yes, tweet is called 'status' rather confusing
        except Exception as e:
            return str(e)
        return 'Sucessfully tweetted status, please check!'

    def get_api(self, cfg):
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)

class SmsPublisher(MediaPublisher):
    '''
    content: String
    phoneNumber: String, format: +6592739580
    retrun: String, a message indicate successful or not
    '''
    def compose_and_publish(self,message='Message not passed in',recipient_list=['+6584393467',]):
        return_message = "Message successfully send to:"
        for recipient in recipient_list:
            return_message += "\n" + self.send(message,recipient=recipient)
        return return_message

    def send(self,message='Message not passed in',recipient=None):
        from twilio.rest.client import TwilioRestClient
        accountSID = 'AC9ae3071c0a5e576c45b3822e7f33e176'
        authToken = 'c65cba6198e425f50f3b1eda3487d984'
        client = TwilioRestClient(accountSID,authToken)
        print(recipient)
        try:
            client.messages.create(body=message, to=recipient, from_='+14692083379' )
        except Exception as e:
            return e.__str__()
        return recipient


