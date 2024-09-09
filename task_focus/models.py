from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    groups = models.ManyToManyField(Group, related_name="worker_set")
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="worker_set"
    )

    class Meta:
        ordering = ["first_name"]
        verbose_name = "worker"
        verbose_name_plural = "workers"


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)
    # priority = models.IntegerField(default=0)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
