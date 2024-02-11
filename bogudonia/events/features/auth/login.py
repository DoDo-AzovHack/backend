import json
from dataclasses import asdict

from django.contrib.postgres import serializers
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from events.dataclasses.responses import Body, Status
from events.objects.User import User


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse(
            data=Body.BAD_REQUEST,
            status=Status.BAD_REQUEST)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except:
        body = request.POST

    try:
        email = body["email"]
        password = body["password"]
    except:
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID)

    try:
        user = (User.objects
                .values('id', 'name', 'about', 'email', 'password', 'role', 'permissions', 'contacts')
                .get(email=email))
    except:
        return JsonResponse(
            data=Body.NOT_FOUND,
            status=Status.NOT_FOUND)

    if user['password'] != User.hash_pass(password):
        return JsonResponse(
            data=Body.BAD_REQUEST,
            status=Status.BAD_REQUEST)

    del user['password']

    data = json.dumps(user)
    return HttpResponse(data, content_type='application/json')

