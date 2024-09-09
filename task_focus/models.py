from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=100)


class Position(models.Model):
    name = models.CharField(max_length=100)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        ordering = ["first_name"]
        verbose_name = "worker"
        verbose_name_plural = "workers"


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)
    # priority = models.IntegerField(default=0)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
