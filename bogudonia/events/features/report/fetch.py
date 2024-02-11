import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from events.dataclasses.responses import Body, Status
from events.objects.Event import Event
from events.objects.Tag import Tag
from events.objects.User import User


@csrf_exempt
def fetch_events(request):
    if request.method != "POST":
        return JsonResponse(
            data=Body.BAD_REQUEST,
            status=Status.BAD_REQUEST)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except:
        body = request.POST

    user: User = User.authorize(body['auth']['email'], body['auth']['password'])

    if not user:
        return JsonResponse(data=Body.AUTHORIZED_FALSE, status=Status.UNAUTHORIZED)

    if body['params'].get('tags'):
        body['params']['tags'] = [
            Tag.objects.get(id=_id) for _id in body['params']['tags']
        ]

    events: list[Event] = Event.fetch(user=user, **body['params'])
    data = json.dumps([
        event.bit_serialize() for event in events
    ])

    return HttpResponse(data, content_type='application/json')
