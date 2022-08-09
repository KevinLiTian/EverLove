""" Register Models """
from django.contrib import admin
from .models import User, Job, Hobby, UserWithHobby

admin.site.register(User)
admin.site.register(Job)
admin.site.register(Hobby)
admin.site.register(UserWithHobby)
