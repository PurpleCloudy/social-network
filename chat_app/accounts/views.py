from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import UserProfile
from django.http import HttpResponse

# Create your views here.

def registration_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
    return render(request, 'accounts/registration_form.html', {'form':form})

