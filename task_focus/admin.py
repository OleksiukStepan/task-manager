from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_focus.models import TaskType, Position, Worker, Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
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
    )


@admin.register(Task)
class Task(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("deadline", "is_complete", "priority",)


admin.site.register(TaskType)
admin.site.register(Position)
