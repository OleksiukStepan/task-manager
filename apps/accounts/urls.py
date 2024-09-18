""" URL patterns for task_manager """

from django.urls import path

from django.urls import path
from .views import login_view, register_user, ResetPassword
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reset-password/", ResetPassword.as_view(), name="reset-password")
]

app_name = "accounts"
