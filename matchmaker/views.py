from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import Profile


def home(request):
    return render(request, 'matchmaker/home.html')


@login_required
def discover(request):
    context = {
        'profiles': Profile.objects.all()
    }
    return render(request, 'matchmaker/discover.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'users/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'users/login.html')
