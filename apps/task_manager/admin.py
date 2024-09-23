from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.task_manager.models import TaskType, Position, Worker, Task, Tag


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    list_filter = UserAdmin.list_filter + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "position",
                )
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "deadline",
        "priority",
        "task_type",
    )
    list_filter = (
        "deadline",
        "is_complete",
        "priority",
        "task_type",
    )
    filter_horizontal = ("assignees",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)


admin.site.register(TaskType)
admin.site.register(Position)
