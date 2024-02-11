from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import CharField, ImageField, ManyToManyField, SmallIntegerField, ForeignKey, DateTimeField, \
    AutoField
from django import forms

from events.objects.Tag import Tag
from events.objects.User import User


class Event(models.Model):
    class Status:
        ON_CONSIDERATION = 0
        CONFIRMED = 1

    class Urgency:
        URGENT = 0
        NOT_SO_URGENT = 1
        NOT_URGENT = 2

        colors = {
            URGENT: 0xF32727,
            NOT_SO_URGENT: 0xFFD600,
            NOT_URGENT: 0x00FF47
        }

    class Paginator:
        request_limit = 20

        @classmethod
        def start(cls, limit):
            return limit - cls.request_limit

        @classmethod
        def limit(cls, page):
            return cls.request_limit * page

    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = CharField(max_length=50)
    description = CharField(max_length=300)
    banner = ImageField(upload_to="events/", null=True)
    tags = ManyToManyField(Tag, related_name='tag_events')
    location = CharField(max_length=100, null=False)
    urgency = SmallIntegerField(default=Urgency.NOT_URGENT)
    status = SmallIntegerField(default=Status.ON_CONSIDERATION)
    timestamp = DateTimeField(auto_now_add=True)
    members = ManyToManyField(User, related_name='member_events')

    @classmethod
    def fetch(cls,
        user: User,
        page: int = 1,
        q: str = None,
        my: bool = False,
        tags: list[Tag] = None,
        urgency: int = None,status: int = None
    ):
        filters = {}
        print(page, q, tags, urgency, status)

        if q:
            filters['title__icontains'] = q
        if tags:
            filters['tags__in'] = tags
        if urgency is not None:
            filters['urgency'] = urgency
        if status is not None:
            filters['status'] = status
        if not page:
            page = 1

        limit = cls.Paginator.limit(page)

        if my:
            events = user.member_events
        else:
            events = cls.objects

        return events.filter(**filters).all()[cls.Paginator.start(limit):limit]

    def serialize(self):
        data = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            banner=None,
            location=self.location,
            status=self.status,
            members_count=self.members.count(),
            members=[],
            actions=[],
            tags=[])

        data['author'] = self.author.serialize()
        data['urgency'] = {
            'level': self.urgency,
            'color': 0x222222
        }

        if self.banner:
            data['banner'] = self.banner.url

        for tag in self.tags.all():
            data['tags'].append(tag.serialize())

        for member in self.members.all():
            data['members'].append(member.serialize())

        for action in self.actions.all():
            data['actions'].append(action.serialize())

        return data

    def bit_serialize(self):
        data = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            banner=None,
            location=self.location,
            status=self.status,
            tags=[])

        data['urgency'] = {
            'level': self.urgency,
            'color': 0x222222
        }

        if self.banner:
            data['banner'] = self.banner.url

        for tag in self.tags.all():
            data['tags'] += tag.serialize()

        return data


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'location', 'urgency')
