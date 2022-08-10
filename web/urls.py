""" URL for Chat App """
from django.urls import path
from . import views

app_name = "web"
urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('spark', views.spark, name="spark"),
    path('filter_api', views.filter_api),
    path('match_api', views.match_api, name="match_api")
]
