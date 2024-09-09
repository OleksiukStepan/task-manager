from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100)
