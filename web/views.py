""" Views """
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import IntegrityError

from .models import User


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
