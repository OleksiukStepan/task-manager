from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from django import forms

from apps.task_manager.models import Worker, TaskType, Position, Task, Tag


COMMON_WIDGET_ATTRS = {"class": "form-control"}


def get_text_input_widget(placeholder):
    return forms.TextInput(
        attrs={**COMMON_WIDGET_ATTRS, "placeholder": placeholder}
    )


class WorkerFormMixin:
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Profile Image",
    )


class MemberCreateForm(WorkerFormMixin, UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                **COMMON_WIDGET_ATTRS,
                "placeholder": "Password",
                "required": True
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                **COMMON_WIDGET_ATTRS,
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
            "username": get_text_input_widget("Username"),
            "first_name": get_text_input_widget("First Name"),
            "last_name": get_text_input_widget("Last Name"),
            "email": forms.EmailInput(
                attrs={
                    **COMMON_WIDGET_ATTRS,
                    "placeholder": "name@company.com",
                }
            ),
            "position": forms.Select(attrs={"class": "form-select"}),
            "phone": get_text_input_widget("+12-345 678 910"),
            "birthday": forms.DateInput(
                attrs={
                    **COMMON_WIDGET_ATTRS,
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


class MemberUpdateForm(WorkerFormMixin, forms.ModelForm):
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
            "name": get_text_input_widget("Enter task name"),
            "description": forms.Textarea(
                attrs={
                    **COMMON_WIDGET_ATTRS,
                    "placeholder": "Enter task description",
                    "rows": 3,
                    "required": False,
                }
            ),
            "deadline": forms.DateInput(
                attrs={
                    **COMMON_WIDGET_ATTRS,
                    "type": "date",
                    "required": False,
                }
            ),
            "priority": forms.Select(
                attrs={**COMMON_WIDGET_ATTRS, "required": False}
            ),
            "task_type": forms.Select(
                attrs={**COMMON_WIDGET_ATTRS, "required": False}
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
            "name": get_text_input_widget("Enter task type name"),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]
        widgets = {
            "name": get_text_input_widget("Enter position name"),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "color"]
        widgets = {
            "name": get_text_input_widget("Enter tag name"),
            "color": forms.TextInput(
                attrs={
                    **COMMON_WIDGET_ATTRS,
                    "placeholder": "Enter tag color",
                    "type": "color",
                }
            ),
        }
