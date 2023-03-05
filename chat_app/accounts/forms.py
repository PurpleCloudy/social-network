from django import forms
from django.contrib.auth import get_user_model


class RegisterForm(forms.Form):
    username = forms.CharField(requered = True, max_length=30)
    email = forms.EmailField(requered = True)
    password = forms.CharField(requered = True,max_length=30)


