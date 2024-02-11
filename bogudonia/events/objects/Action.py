from django import forms
from django.db import models
from django.db.models import AutoField, CharField, ImageField, ForeignKey, DateTimeField, SmallIntegerField

from events.objects.Event import Event
from events.objects.User import User


class Action(models.Model):
    class Status:
        ON_CONSIDERATION = 0
        CONFIRMED = 1

    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=models.CASCADE, null=True)
    event = ForeignKey(Event, on_delete=models.CASCADE, related_name='actions', null=True)
    description = CharField(max_length=100)
    photo = ImageField(upload_to="actions/", null=True)
    status = SmallIntegerField(default=Status.ON_CONSIDERATION)
    timestamp = DateTimeField(auto_now_add=True)

    def serialize(self):
        data = dict(
            id=self.id,
            event=self.event.id,
            author=self.author.serialize(),
            description=self.description,
            timestamp=str(self.timestamp)
        )

        if self.photo:
            data['photo'] = self.photo.url

        return data


class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ('description',)
