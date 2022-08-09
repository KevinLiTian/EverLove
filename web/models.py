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

LIFE_STYLE_CHOICES = [('NA', ''), ('HED', 'hedonistic'),
                      ('ADV', 'adventuristic'), ('IND', 'individualistic'),
                      ('PRO', 'promethean')]


class Job(models.Model):
    """ All Job """
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Hobby(models.Model):
    """ All Hobbies """
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

    description = models.TextField(blank=True, null=True)

    sexuality = models.CharField(max_length=32,
                                 choices=GENDER_CHOICES,
                                 default='NA')

    lifestyle = models.CharField(max_length=3,
                                 choices=LIFE_STYLE_CHOICES,
                                 default='NA')

    def __str__(self):
        return f"{self.username}"


class UserWithHobby(models.Model):
    """ Link User to Hobbies """
    hobby = models.ForeignKey(Hobby,
                              on_delete=models.CASCADE,
                              related_name="usrs")
    usr = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name="hobbies")

    def __str__(self):
        return f"{self.usr} has hobby of {self.hobby}"
