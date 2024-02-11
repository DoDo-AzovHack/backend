import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from events.dataclasses.responses import Body, Status
from events.objects.Event import Event
from events.objects.User import User


@csrf_exempt
def delete_event(request):
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
        event_id = body['event']
    except:
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID)

    user: User = User.authorize(email, password)
    if not user:
        return JsonResponse(
            data=Body.AUTHORIZED_FALSE,
            status=Status.UNAUTHORIZED)

    try:
        event = Event.objects.get(id=event_id)
    except:
        return JsonResponse(
            data=Body.NOT_FOUND,
            status=Status.NOT_FOUND)

    if user != event.author:
        return JsonResponse(
            data=Body.FORBIDDEN,
            status=Status.FORBIDDEN)

    event.delete()
    return JsonResponse(
        data=Body.DELETED,
        status=Status.DELETED)
