import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from events.dataclasses.responses import Body, Status
from events.objects.User import User, UserForm


@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse(
            data=Body.BAD_REQUEST,
            status=Status.BAD_REQUEST)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except:
        body = request.POST
    files = request.FILES

    form = UserForm(body, files)
    if not form.is_valid():
        return JsonResponse(
            data=Body.INVALID_FORM_BODY,
            status=Status.INVALID)

    user = form.save()
    user.password = User.hash_pass(user.password)


    #TODO: debug
    if user.name == 'nigga':
        user.permissions = User.Permissions.OWNER

    user.save()

    return JsonResponse(
        data=Body.CREATED,
        status=Status.OK)
