from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=100)


class Position(models.Model):
    name = models.CharField(max_length=100)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)



