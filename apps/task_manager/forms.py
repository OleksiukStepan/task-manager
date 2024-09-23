from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from django import forms

from apps.task_manager.models import Worker, TaskType, Position, Task, Tag


class MemberCreateForm(UserCreationForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Profile Image",
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password", "required": True}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
                "required": True,
            }
        ),
    )

    class Meta:
        model = Worker
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "birthday",
            "male",
            "email",
            "phone",
            "position",
            "profile_image",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Username",
                    "required": True,
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First Name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name@company.com",
                }
            ),
            "position": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+12-345 678 910",
                }
            ),
            "birthday": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "dd/mm/yyyy",
                    "type": "date",
                }
            ),
            "male": forms.Select(
                attrs={
                    "class": "form-select mb-0",
                    "aria-label": "Gender select example",
                },
                choices=[(None, "Gender"), (False, "Female"), (True, "Male")],
            ),
        }


class MemberUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Profile Image",
    )

    class Meta(MemberCreateForm.Meta):
        fields = [
            "username",
            "first_name",
            "last_name",
            "position",
            "birthday",
            "male",
            "email",
            "phone",
            "profile_image",
        ]


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
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task name",
                    "required": False,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task description",
                    "rows": 3,
                    "required": False,
                }
            ),
            "deadline": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "required": False}
            ),
            "priority": forms.Select(
                attrs={"class": "form-control", "required": False}
            ),
            "task_type": forms.Select(
                attrs={"class": "form-control", "required": False}
            ),
            "is_complete": forms.CheckboxInput(
                attrs={"class": "form-check-input", "required": False}
            ),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("The deadline cannot be in the past")
        return deadline


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search",
            }
        ),
    )


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control mb-2",
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
                    "class": "form-control mb-2",
                    "placeholder": "Enter position name",
                }
            )
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "color"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control mb-2",
                    "placeholder": "Enter position name",
                }
            ),
            "color": forms.TextInput(
                attrs={
                    "class": "form-control mb-2",
                    "placeholder": "Enter tag color",
                    "type": "color",
                }
            ),
        }
