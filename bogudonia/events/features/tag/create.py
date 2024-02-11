import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from events.dataclasses.responses import Body, Status
from events.objects.Tag import Tag
from events.objects.User import User


@csrf_exempt
def create_tag(request):
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
        name = body['name']
        color = body['color']
    except:
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID)

    user: User = User.authorize(email, password)
    if not user:
        return JsonResponse(data=Body.AUTHORIZED_FALSE, status=Status.UNAUTHORIZED)
    if user.permissions != User.Permissions.OWNER:
        return JsonResponse(data=Body.FORBIDDEN, status=Status.FORBIDDEN)

    tag = Tag.objects.create(name=name, color=color)
    data = json.dumps(tag.serialize())
    return HttpResponse(data, content_type='application/json')
