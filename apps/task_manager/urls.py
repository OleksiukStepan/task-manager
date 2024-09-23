""" URL patterns for task_manager """

from django.conf.urls.static import static
from django.urls import path

from core import settings
from .views import (
    index,
    set_worker_status,
    add_tag,
    add_task_type,
    remove_task_type,
    add_position,
    remove_position,
    SaveTagsView,
    # RemoveTagView,
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
    path("task/<int:pk>/save-tags/", SaveTagsView.as_view(), name="save_tags"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("worker/<int:pk>/set_status/", set_worker_status, name="set_worker_status"),
    path("add-task-type/", add_task_type, name="add_task_type"),
    path(
        "remove-task-type/<int:task_type_id>/",
        remove_task_type,
        name="remove_task_type",
    ),
    path("add-position/", add_position, name="add_position"),
    path("remove-position/<int:position_id>/", remove_position, name="remove_position"),
    path("add-tag/", add_tag, name="add_tag"),
    # path("tag/<int:tag_id>/delete/", RemoveTagView.as_view(), name="remove_tag"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "task_manager"
