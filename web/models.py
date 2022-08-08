""" Database """
from django.contrib.auth.models import AbstractUser
from django.db import models

PERSONALITY_CHOICES = [('NA', ''), ('INTP', 'INTP'), ('INTJ', 'INTJ'),
                       ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'), ('INFJ', 'INFJ'),
                       ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
                       ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'),
                       ('ESFJ', 'ESFJ'), ('ISTP', 'ISTP'), ('ISFP', 'ISFP'),
                       ('ESTP', 'ESTP'), ('ESFP', 'ESFP')]

GENDER_CHOICES = [('NA', ''), ('Male', 'Male'), ('Female', 'Female'),
                  ('Other', 'Other'), ('PNA', 'Prefer no to answer')]


class Job(models.Model):
    """ All Job """
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    """ User Info """
    fullname = models.CharField(max_length=64, default='')

    gender = models.CharField(max_length=32,
                              choices=GENDER_CHOICES,
                              default='NA')

    age = models.IntegerField(blank=True, null=True)

    personality = models.CharField(max_length=4,
                                   choices=PERSONALITY_CHOICES,
                                   default='NA')

    job = models.ForeignKey(Job,
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,
                            related_name="people")

    description1 = models.TextField(blank=True, null=True)

    sexuality = models.CharField(max_length=32,
                                 choices=GENDER_CHOICES,
                                 default='NA')

    description2 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username}"
