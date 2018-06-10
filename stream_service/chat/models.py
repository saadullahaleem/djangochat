import datetime
from django.db import models
from custom_user.models import AbstractEmailUser


class User(AbstractEmailUser):
    alias = models.CharField(max_length=20)


class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
