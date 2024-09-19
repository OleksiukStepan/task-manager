""" URL patterns for task_manager """

from django.urls import path

from django.urls import path
from .views import (
    login_view,
    register_user,
    ResetPassword,
    terms_and_conditions
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reset-password/", ResetPassword.as_view(), name="reset_password"),
    path(
        "terms-and-conditions/",
        terms_and_conditions,
        name="terms_and_conditions"
    ),
]

app_name = "accounts"
