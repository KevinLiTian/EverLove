""" Views """
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import PERSONALITY_CHOICES, GENDER_CHOICES, User, Job


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
@login_required(login_url="web:login")
def profile(request, username):
    """ User Profile Page """
    if request.method == "GET":
        usr = User.objects.get(username=username)
        return render(
            request, "web/profile.html", {
                "usr": usr,
                "personalities": PERSONALITY_CHOICES,
                "genders": GENDER_CHOICES
            })

    # API
    elif request.method == "PUT":
        data = json.loads(request.body)
        fullname = data["fullname"]
        gender = data["gender"]
        age = data["age"]
        personality = data["personality"]
        job = data["job"]
        sexuality = data["sexuality"]
        description1 = data["description1"]
        description2 = data["description2"]

        usr = User.objects.get(username=username)
        usr.fullname = fullname
        usr.gender = gender
        usr.age = age
        usr.personality = personality

        if job != '':
            job = job.lower()
            job_obj = Job.objects.filter(name=job)
            if job_obj:
                usr.job = job_obj[0]
            else:
                usr.job = Job.objects.create(name=job)

        usr.sexuality = sexuality
        usr.description1 = description1
        usr.description2 = description2
        usr.save()

        return JsonResponse({"Success": "Data updated."}, status=200)

    return render(
        request, "web/profile.html", {
            "usr": usr,
            "personalities": PERSONALITY_CHOICES,
            "genders": GENDER_CHOICES
        })
