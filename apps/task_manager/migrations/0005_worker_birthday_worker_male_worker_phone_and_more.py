# Generated by Django 5.1.1 on 2024-09-19 19:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0004_task_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="worker",
            name="birthday",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="worker",
            name="male",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="worker",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="assignees",
            field=models.ManyToManyField(
                null=True, related_name="tasks", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]