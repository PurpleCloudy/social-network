from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import SubscribeModel
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.
@login_required(login_url="/login/")
def subscribing_view(request, pk):
    try:
        SubscribeModel.objects.get(self_user = request.user, other_user = User.objects.get(id=pk))
    except:
        if pk != request.user.id:
            sub = SubscribeModel(self_user = request.user, other_user = User.objects.get(id=pk))
            sub.save()
    return redirect(reverse('index'))
