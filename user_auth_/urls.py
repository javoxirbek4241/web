from django.urls import path
from.views import *
urlpatterns = [
    path('regis/', RegisterApi.as_view()),
    path("login/", LoginApi.as_view(), name="login"),
    path("logout/", LogoutApi.as_view(), name="logout"),
]