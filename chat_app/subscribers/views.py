from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import SubscribeModel
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.
@login_required(login_url="/login/")
def subscribing_view(request, pk):
    if request.method == "POST":
        try:
            SubscribeModel.objects.get(self_user = request.user, other_user = User.objects.get(id=pk))
        except:
            sub = SubscribeModel(self_user = request.user, other_user = User.objects.get(id=pk))
            sub.save()
    return render(request, reverse('index'))