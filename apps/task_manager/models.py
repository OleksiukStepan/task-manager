from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # profile_image = models.ImageField(
    #     upload_to=worker_image_file_path,
    #     blank=True,
    #     null=True
    # )

    class Meta:
        ordering = ["first_name"]
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Task(models.Model):
    CHOICES = [(1, "Urgent"), (2, "High"), (3, "Medium"), (4, "Low")]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)
    priority = models.IntegerField(choices=CHOICES, default=3)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
