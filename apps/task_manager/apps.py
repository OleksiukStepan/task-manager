from django.apps import AppConfig


class TaskManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.task_manager"

    def ready(self):
        import apps.task_manager.signals
