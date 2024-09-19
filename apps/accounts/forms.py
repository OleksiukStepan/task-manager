from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.task_manager.models import Worker


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    remember_me = forms.BooleanField(required=False, label='Remember me')


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))
    agree_terms = forms.BooleanField(
        required=True, label="I agree to the terms and conditions"
    )

    class Meta:
        model = Worker
        fields = ('username', 'email', 'password1', 'password2', 'agree_terms')

    def clean_agree_terms(self):
        agree = self.cleaned_data.get("agree_terms")
        if not agree:
            raise forms.ValidationError(
                "You must agree to the terms and conditions to register."
            )
        return agree
