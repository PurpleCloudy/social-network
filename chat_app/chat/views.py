from django.shortcuts import render
from .forms import ChatForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index_view(request):
    form = ChatForm(request.POST or None)
    return render(request, 'index.html', {'form':form})

@login_required(login_url="/login/")
def sending_view(request):
    print(request.POST)