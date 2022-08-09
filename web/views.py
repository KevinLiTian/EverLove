""" Views """
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import PERSONALITY_CHOICES, GENDER_CHOICES, LIFE_STYLE_CHOICES, \
                    User, Job, Hobby, UserWithHobby


def index(request):
    """ Index View """
    return render(request, 'web/index.html')


def login_view(request):
    """ Login View
    If POST request, then log user in if information matches database
    If GET request, render the login page
    """
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("web:index")

        return render(request, "web/login.html",
                      {"message": "Invalid username and/or password."})

    # GET
    return render(request, "web/login.html")


def logout_view(request):
    """ Logout View """
    logout(request)
    return redirect("web:index")


def register(request):
    """ Register View
    If POST request, try to register a new user
    If GET request, render the registration form
    """
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "web/register.html",
                          {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password)
            user.save()
        except IntegrityError:
            return render(request, "web/register.html",
                          {"message": "Username already taken."})

        login(request, user)
        return redirect("web:index")

    # GET
    return render(request, "web/register.html")


@csrf_exempt
def profile(request, username):
    """ User Profile Page """
    if request.method == "GET":
        usr = User.objects.get(username=username)
        hobbies = [usr_hobby.hobby for usr_hobby in usr.hobbies.all()]
        hobby1 = (hobbies[0] if len(hobbies) >= 1 else None)
        hobby2 = (hobbies[1] if len(hobbies) >= 2 else None)
        hobby3 = (hobbies[2] if len(hobbies) == 3 else None)

        return render(
            request, "web/profile.html", {
                "usr": usr,
                "hobby1": hobby1,
                "hobby2": hobby2,
                "hobby3": hobby3,
                "personalities": PERSONALITY_CHOICES,
                "genders": GENDER_CHOICES,
                "lifestyles": LIFE_STYLE_CHOICES
            })

    # API
    if request.method == "PUT":
        data = json.loads(request.body)
        fullname = data["fullname"]
        gender = data["gender"]
        age = data["age"]
        personality = data["personality"]
        job = data["job"]
        sexuality = data["sexuality"]
        lifestyle = data["lifestyle"]
        description = data["description"]
        hobbies = (data["hobby1"], data["hobby2"], data["hobby3"])

        usr = User.objects.get(username=username)

        usr.fullname = fullname
        usr.gender = gender
        usr.age = age
        usr.personality = personality
        usr.sexuality = sexuality
        usr.lifestyle = lifestyle
        usr.description = description

        # Job processing
        if job != '':
            job = job.lower()
            job_obj = Job.objects.filter(name=job)
            if job_obj:
                usr.job = job_obj[0]
            else:
                usr.job = Job.objects.create(name=job)

        # Hobby Processing
        for usr_hobby in usr.hobbies.all():
            usr_hobby.delete()

        for hobby in hobbies:
            if hobby == '':
                continue

            hobby = hobby.lower()
            hobby_obj = Hobby.objects.filter(name=hobby)
            if not hobby_obj:
                hobby_obj = Hobby.objects.create(name=hobby)
                UserWithHobby.objects.create(hobby=hobby_obj, usr=usr)

            else:
                UserWithHobby.objects.create(hobby=hobby_obj[0], usr=usr)

        usr.save()

        return JsonResponse({"Success": "Data updated."}, status=200)

    return JsonResponse({"error": "GET or PUT"}, status=403)


def spark(request):
    """ Match Page """
    hobbies = Hobby.objects.all()
    usrs = User.objects.all()
    return render(
        request, 'web/spark.html', {
            "personalities": PERSONALITY_CHOICES,
            "genders": GENDER_CHOICES,
            "lifestyles": LIFE_STYLE_CHOICES,
            "hobbies": hobbies,
            "usrs": usrs
        })
