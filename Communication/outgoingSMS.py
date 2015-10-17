'''
6F/B/sT6kcp+mWI0FnlNQal+lzE9brHWWsnF3u9I
@author: Zhou


DO THIS FIRST 
installation guide:
run this in terminal: pip install twilio
'''


from twilio.rest import TwilioRestClient
'''
content: String
phoneNumber: String, format: +6592739580
retrun: String, a message indicate successful or not
'''

def sendingSMS(content = 'Hello! 3003 test',phoneNumber = '+6592739580'):
    accountSID = 'AC9ae3071c0a5e576c45b3822e7f33e176'
    authToken = 'c65cba6198e425f50f3b1eda3487d984'
    client = TwilioRestClient(accountSID,authToken)
    print(phoneNumber)
    try:
        client.messages.create(body = content , to = phoneNumber,  from_ = '+14692083379' )
    except Exception as e:
        return e.__str__()
    return 'Message successfully sent to '+phoneNumber