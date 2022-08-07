""" Database """
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ User Info """
    fullname = models.CharField(max_length=64, blank=True)
    birth = models.DateField(auto_now_add=False,
                             auto_now=False,
                             blank=True,
                             null=True)
    description = models.TextField(blank=True)
    age = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.username}"
