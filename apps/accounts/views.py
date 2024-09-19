from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                else:
                    # Set session to expire in 7 days
                    request.session.set_expiry(604800)
                return redirect("/")
            else:
                msg = 'Invalid credentials'

        else:
            msg = 'Error validating the form'

    return render(
        request,
        "accounts/login.html",
        {"form": form, "msg": msg}
    )


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created - please <a href="accounts:login">login</a>.'
            success = True

            return redirect("accounts/login/")
        else:
            msg = 'Form is not valid'

    else:
        form = SignUpForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form, "msg": msg, "success": success}
    )


class ResetPassword(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/reset-password.html"
    success_url = reverse_lazy("accounts:login")
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(
            self.request, "Your password was successfully changed!"
        )
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Current Password',
            'id': 'old_password'
        })
        form.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New Password',
            'id': 'new_password1'
        })
        form.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
            'id': 'new_password2'
        })
        return form
