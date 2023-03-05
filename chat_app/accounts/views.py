from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import UserProfile

# Create your views here.

def index(request, *args, **kwargs):
    return render(request, 'registration_form.html')