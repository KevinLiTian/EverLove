""" Database """
from django.contrib.auth.models import AbstractUser
from django.db import models

PERSONALITY_CHOICES = [('NA', ''), ('INTP', 'INTP'), ('INTJ', 'INTJ'),
                       ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'), ('INFJ', 'INFJ'),
                       ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
                       ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'),
                       ('ESFJ', 'ESFJ'), ('ISTP', 'ISTP'), ('ISFP', 'ISFP'),
                       ('ESTP', 'ESTP'), ('ESFP', 'ESFP')]

GENDER_CHOICES = [('NA', ''), (0, 'Male'), (1, 'Female'), (2, 'Other'),
                  (3, 'Prefer no to answer')]


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

    description = models.TextField(default='')

    def __str__(self):
        return f"{self.username}"
