from django.shortcuts import render


from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import json

def index(request):
    return render(request, 'index.html')


#category: sys_log, incident, update, dispatch, proposed_dispatch
def publish(serializer, category, request):
    message = {}
    redis_publisher = RedisPublisher(facility = 'pushes', broadcast = True)
    existing_message = redis_publisher.fetch_message( request , 'pushes')
    if existing_message:
        message = json.loads(existing_message)
    message[category] = serializer.data
    redis_publisher.publish_message(RedisMessage(json.dumps(message)))