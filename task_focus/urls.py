""" URL patterns for task_focus """

from django.urls import path

from .views import index

urlpatterns = [
    path("", index, name="home"),
]

app_name = "task_focus"
