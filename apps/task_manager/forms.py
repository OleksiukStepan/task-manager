from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput, EmailInput, Select, DateInput

from apps.task_manager.models import Worker, TaskType, Position


class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = [
            "first_name",
            "last_name",
            "birthday",
            "male",
            "email",
            "phone",
            "position",
        ]
        widgets = {
            "first_name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First Name",
                }
            ),
            "last_name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name@company.com",
                }
            ),
            "position": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "phone": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+12-345 678 910",
                }
            ),
            "birthday": DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "dd/mm/yyyy",
                    "type": "date",
                }
            ),
            "male": Select(
                attrs={
                    "class": "form-select mb-0",
                    "aria-label": "Gender select example",
                },
                choices=[(None, "Gender"), (False, "Female"), (True, "Male")],
            ),
        }


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task type name",
                }
            )
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter position name",
                }
            )
        }
