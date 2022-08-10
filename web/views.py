""" Views """
import json
import random
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
            user = User.objects.create_user(username=username,
                                            password=password)
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

        usr.fullname = fullname.strip()
        usr.gender = gender
        usr.age = age
        usr.personality = personality
        usr.sexuality = sexuality
        usr.lifestyle = lifestyle
        usr.description = description.strip()

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

    if request.user.is_authenticated:
        usrs = usrs.exclude(username=request.user.username)

    usrs = list(usrs)

    if len(usrs) > 10:
        usrs = random.sample(usrs, 10)

    return render(
        request, 'web/spark.html', {
            "personalities": PERSONALITY_CHOICES,
            "genders": GENDER_CHOICES,
            "lifestyles": LIFE_STYLE_CHOICES,
            "hobbies": hobbies,
            "usrs": usrs
        })


@csrf_exempt
def filter_api(request):
    """ Filter API """
    if request.method == "POST":
        data = json.loads(request.body)
        gender = data["gender"]
        age = data["age"]
        personality = data["personality"]
        lifestyle = data["lifestyle"]
        hobby = data["hobby"]

        selected_users = User.objects.all()
        if gender != 'NA':
            selected_users = selected_users.filter(gender=gender)

        if age != '0':
            if age == '1':
                selected_users = selected_users.filter(age__lt=20)
            elif age == '8':
                selected_users = selected_users.filter(age__gte=50)
            else:
                low = 20 + (int(age) - 2) * 5
                high = low + 4
                selected_users = selected_users.filter(age__gte=low).filter(
                    age__lte=high)

        if personality != 'NA':
            selected_users = selected_users.filter(personality=personality)

        if lifestyle != 'NA':
            selected_users = selected_users.filter(lifestyle=lifestyle)

        if hobby != '0':
            hobby_obj = Hobby.objects.get(name=hobby)
            usr_with_hobby = [
                usr_hobby.usr for usr_hobby in hobby_obj.usrs.all()
            ]

            for usr in selected_users:
                if usr not in usr_with_hobby:
                    selected_users = selected_users.exclude(
                        username=usr.username)

        if request.user.is_authenticated:
            selected_users = selected_users.exclude(
                username=request.user.username)

        selected_users = list(selected_users)

        if len(selected_users) > 10:
            selected_users = random.sample(selected_users, 10)

        return JsonResponse([usr.serialize() for usr in selected_users],
                            safe=False)


@login_required(login_url="web:login")
def match_api(request):
    """ Match API """
    usr = User.objects.get(username=request.user.username)

    gender = usr.gender
    personality = usr.personality
    sexuality = usr.sexuality
    lifestyle = usr.lifestyle
    hobbies = [usr_hobby.hobby for usr_hobby in usr.hobbies.all()]

    selected_users = User.objects.all()
    selected_users = selected_users.filter(gender=sexuality).filter(
        sexuality=gender)

    comparison_dict = {candidate: 0 for candidate in selected_users}

    for candidate in comparison_dict:
        if (candidate.personality.startswith('E') and personality.startswith('I')) or \
            (candidate.personality.startswith('I') and personality.startswith('E')):
            comparison_dict[candidate] += 1

        if candidate.lifestyle == lifestyle:
            comparison_dict[candidate] += 1

        candidate_hobbies = [
            candidate_hobby.hobby
            for candidate_hobby in candidate.hobbies.all()
        ]

        comparison_dict[candidate] += len(
            list(set(hobbies).intersection(candidate_hobbies)))

    selected_users = [
        pair[0] for pair in sorted(
            comparison_dict.items(), key=lambda item: item[1], reverse=True)
    ]

    return JsonResponse([usr.serialize() for usr in selected_users],
                        safe=False)
