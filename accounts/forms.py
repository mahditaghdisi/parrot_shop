from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل (اختیاری)"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "نام کاربری"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "رمز عبور"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "تکرار رمز عبور"})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "نام کاربری"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "رمز عبور"})
