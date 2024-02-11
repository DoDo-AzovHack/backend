import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from events.dataclasses.responses import Status, Body
from events.objects.Action import Action
from events.objects.User import User


@csrf_exempt
def confirm_action(request):
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
        action_id = body['action']
    except:
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID)

    user: User = User.authorize(email, password)
    if not user:
        return JsonResponse(
            data=Body.AUTHORIZED_FALSE,
            status=Status.UNAUTHORIZED)

    if user.permissions >= User.Permissions.USER:
        return JsonResponse(
            data=Body.FORBIDDEN,
            status=Status.FORBIDDEN)

    try:
        action = Action.objects.get(id=action_id)
    except:
        return JsonResponse(
            data=Body.NOT_FOUND,
            status=Status.NOT_FOUND)

    action.status = Action.Status.CONFIRMED
    action.save()
    action.event.members.add(user)

    return JsonResponse(
        data=Body.UPDATED,
        status=Status.OK)
