from django.db import models
from django.db.models import CharField, AutoField, IntegerField


class Tag(models.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=30, unique=True, null=False)
    color = CharField(max_length=6, null=False)

    def serialize(self):
        return dict(key=self.id, label=self.name, color=self.color)
