""" URL patterns for task_manager """

from django.urls import path

from .views import (
    index,
    TaskListView,
)


urlpatterns = [
    path("", index, name="home"),
    path("tasks/", TaskListView.as_view(), name="task-list")
    # path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    # path('members/', MemberListView.as_view(), name='member_list'),
    # path('members/<int:pk>/', MemberListView.as_view(), name='member_detail'),
]

app_name = "task_manager"
