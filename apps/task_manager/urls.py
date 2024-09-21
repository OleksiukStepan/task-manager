""" URL patterns for task_manager """
from django.conf.urls.static import static
from django.urls import path

from core import settings
from .views import (
    index,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    MemberListView,
    MemberCreateView,
    MemberDetailView,
    MemberUpdateView,
    MemberDeleteView,
)


urlpatterns = [
    path("", index, name="home"),
    path("members/", MemberListView.as_view(), name="member_list"),
    path("members/create/", MemberCreateView.as_view(), name="member_create"),
    path("members/<int:pk>/", MemberDetailView.as_view(), name="member_detail"),
    path("members/<int:pk>/update/", MemberUpdateView.as_view(), name="member_update"),
    path("members/<int:pk>/delete/", MemberDeleteView.as_view(), name="member_delete"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "task_manager"
