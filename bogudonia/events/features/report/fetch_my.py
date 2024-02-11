import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from events.dataclasses.responses import Body, Status
from events.objects.Event import Event
from events.objects.User import User


@csrf_exempt
def fetch_my_events(request):
    if request.method != "POST":
        return JsonResponse(
            data=Body.BAD_REQUEST,
            status=Status.BAD_REQUEST)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except:
        body = request.POST

    try:
        email = body['auth']["email"]
        password = body['auth']["password"]
    except:
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID)

    user: User = User.authorize(email, password)
    if not user:
        return JsonResponse(
            data=Body.AUTHORIZED_FALSE,
            status=Status.UNAUTHORIZED)

    events = Event.objects.filter(author=user).all()
    data = json.dumps([event.bit_serialize() for event in events])
    return HttpResponse(data, content_type='application/json')
