import hashlib
from dataclasses import dataclass
from json import JSONEncoder

from django.db import models
from django.db.models import CharField, EmailField, SmallIntegerField, IntegerField, AutoField, ImageField
from django import forms


class User(models.Model):
    class Permissions:
        OWNER = 0
        MODERATOR = 1
        USER = 2

    class Roles:
        GOVERNMENT = 0
        PROPERTY_OWNER = 1
        ECOLOGIST = 2
        ACTIVIST = 3
        RESIDENT = 4
        TOURIST = 5

    id = AutoField(primary_key=True)
    icon = ImageField(upload_to="icons/", null=False)
    name = CharField(max_length=15, null=False)
    about = CharField(max_length=100, default="")
    email = EmailField(null=False, unique=True)
    password = CharField(max_length=100, null=False)
    role = SmallIntegerField(default=Roles.TOURIST)
    permissions = SmallIntegerField(default=Permissions.USER)
    contacts = CharField(max_length=300)

    @classmethod
    def authorize(cls, email: str, password: str):
        try:
            user = cls.objects.get(email=email)
        except:
            return None

        if user.password != cls.hash_pass(password):
            return None

        return user

    def serialize(self):
        data = dict(
            id=self.id,
            icon=None,
            name=self.name,
            about=self.about,
            email=self.email,
            role=self.role,
            permissions=self.permissions,
            contacts=self.contacts
        )

        if self.icon:
            data['icon'] = self.icon.url

        return data

    @staticmethod
    def hash_pass(password: str):
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        return sha256.hexdigest()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'role')
