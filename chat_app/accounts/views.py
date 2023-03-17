from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from .models import UserProfile
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def registration_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create(username=username, email=email, password=password)
            profile = UserProfile.objects.create(profile=user)
            profile.save()
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'accounts/registration_form.html', {'form':form})

def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=user_name, password=password)
            if user:
                login(request, user)
                return redirect("/")
            else:
                return redirect("login/")
    else:
        form = LoginForm()  
    return render(request, 'accounts/login_form.html', {'form':form, 'login':True})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('logout'))

@login_required(login_url="/login/")
def profile_view(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'profile':user})
    

