from django.utils import timezone

from django import forms
from django.forms import TextInput, EmailInput, Select, DateInput

from apps.task_manager.models import Worker, TaskType, Position, Task


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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "is_complete",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Enter task name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task description",
                    "rows": 3,
                }
            ),
            "deadline": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "task_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "is_complete": forms.CheckboxInput(
                attrs={"class": "form-check-input"}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("The deadline cannot be in the past")
        return deadline


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
