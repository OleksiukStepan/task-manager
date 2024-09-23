import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = (
        f"{timezone.now().strftime('%Y%m%d%H%M%S')}"
        f"_{instance.username}.{ext}"
    )
    return os.path.join("profile_images", filename)


class Worker(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    male = models.BooleanField(null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    profile_image = models.ImageField(
        upload_to=user_directory_path, max_length=255, blank=True, null=True
    )

    class Meta:
        ordering = ["first_name"]
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def get_absolute_url(self):
        return reverse(
            "task_manager:member_detail", kwargs={"pk": self.id}
        )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#FFFFFF")

    def __str__(self):
        return self.name


class Task(models.Model):
    CHOICES = [(1, "Urgent"), (2, "High"), (3, "Medium"), (4, "Low")]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)
    priority = models.IntegerField(choices=CHOICES, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.ForeignKey(
        TaskType, on_delete=models.SET_NULL, null=True, blank=True
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks",
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tags",
        blank=True,
    )

    def get_absolute_url(self):
        return reverse(
            "task_manager:task_detail", kwargs={"pk": self.id}
        )

    def __str__(self):
        return self.name
