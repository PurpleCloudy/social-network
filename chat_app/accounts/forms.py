from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

class RegisterForm(forms.Form):
    username = forms.CharField(label = 'Имя', required = True, max_length=30)
    email = forms.EmailField(label = 'Эл. почта', required = True)
    password = forms.CharField(label = 'Пароль', required = True, max_length=30)

class LoginForm(forms.Form):
    username = forms.CharField(label='логин', required=True, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(),label = 'Пароль', required = True, max_length=30)


