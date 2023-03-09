from django import forms
from django.contrib.auth import get_user_model


class RegisterForm(forms.Form):
    username = forms.CharField(label = 'Имя', required = True, max_length=30)
    email = forms.EmailField(label = 'Эл. почта', required = True)
    password = forms.CharField(label = 'Пароль', required = True, max_length=30)


