from django import forms
from django.contrib.auth import get_user_model

from apps.task_manager.models import Worker


class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = "__all__"
