import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from events.dataclasses.responses import Status, Body
from events.objects.Event import EventForm, Event
from events.objects.Tag import Tag
from events.objects.User import User


@csrf_exempt
def create_event(request):
    if request.method != "POST":
        return JsonResponse(
            data=Body.BAD_REQUEST,
            status=Status.BAD_REQUEST)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except:
        body = request.POST
    files = request.FILES

    try:
        email = body['auth']["email"]
        password = body['auth']["password"]
    except:
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID)

    author: User = User.authorize(email, password)
    if not author:
        return JsonResponse(
            data=Body.AUTHORIZED_FALSE,
            status=Status.UNAUTHORIZED)

    form = EventForm(body, files)
    if not form.is_valid():
        print(form.errors)
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID)

    event: Event = form.save()
    event.author = author
    event.members.add(author)
    event.save()

    data = event.serialize()

    tags = body.get('tags')
    print(tags)
    if tags:
        for tag_id in tags:

            try:
                tag = Tag.objects.get(id=tag_id)
                print(tag.serialize())
                event.tags.add(tag)
                data['tags'] += tag.serialize()
            except:
                continue

    return HttpResponse(
        json.dumps(data),
        content_type='application/json')
