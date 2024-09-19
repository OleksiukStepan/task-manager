""" URL patterns for task_manager """

from django.urls import path

from .views import (
    index,
    TaskListView,
    MemberListView,
    MemberDetailView,

)


urlpatterns = [
    path("", index, name="home"),
    path('members/', MemberListView.as_view(), name='member_list'),
    path("members/<int:pk>/", MemberDetailView.as_view(), name="member-detail"),
    path("tasks/", TaskListView.as_view(), name="task_list")
    # path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    # path('members/<int:pk>/', MemberListView.as_view(), name='member_detail'),
]

app_name = "task_manager"
