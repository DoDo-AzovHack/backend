import json


from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from events.dataclasses.responses import Body, Status
from events.objects.Tag import Tag
from events.objects.User import User


@csrf_exempt
def fetch_tag(request):
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

    tags = Tag.objects.all()
    data = json.dumps([tag.serialize() for tag in tags])
    return HttpResponse(data, content_type='application/json')
