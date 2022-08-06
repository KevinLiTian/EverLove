""" Database """
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """ User Info """
    fullname = models.CharField(max_length=64, default='None')
    birth = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.fullname}"
