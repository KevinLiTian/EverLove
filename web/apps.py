""" Register App """
from django.apps import AppConfig


class WebConfig(AppConfig):
    """ Configuration """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'
