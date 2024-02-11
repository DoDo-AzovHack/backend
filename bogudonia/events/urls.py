from django.urls import path

from events.features.action.create import create_action
from events.features.auth.login import login
from events.features.auth.register import register
from events.features.report.confirm import confirm_event
from events.features.report.create import create_event
from events.features.report.delete import delete_event
from events.features.report.fetch import fetch_events
from events.features.report.fetch_my import fetch_my_events
from events.features.report.fetch_one import fetch_one_event
from events.features.tag.create import create_tag
from events.features.tag.fetch import fetch_tag

urlpatterns = [
    path('auth/login', login),
    path('auth/register', register),

    path('event/create', create_event),
    path('event/confirm', confirm_event),
    path('event/fetch', fetch_events),
    path('event/fetch_one', fetch_one_event),
    path('event/fetch_my', fetch_my_events),
    path('event/delete', delete_event),

    path('action/create', create_action),

    path('tag/create', create_tag),
    path('tag/fetch/', fetch_tag),
]
