from django.shortcuts import render, redirect
from django.urls import reverse_lazy


# Create your views here.

def index(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse_lazy('users:profile'))
    return render(request, 'main/index.html')
