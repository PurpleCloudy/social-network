from django.shortcuts import render, redirect
from .forms import ChatForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import ChatModel

# Create your views here.
def index_view(request):
    messages = ChatModel.objects.all()
    form = ChatForm(request.POST or None)
    return render(request, 'index.html', {'form':form, 'messages':messages})

@login_required(login_url="/login/")
def send_view(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            obj = ChatModel(user=request.user, text=form.cleaned_data['text'])
            obj.save()
    return redirect(reverse('index'))