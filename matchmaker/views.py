from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from users.models import Profile


@ensure_csrf_cookie
def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'matchmaker/home.html')


@login_required
def discover(request):
    context = {
        'profiles': Profile.objects.all()
    }
    return render(request, 'matchmaker/discover.html', context)


@login_required
def matches(request):
    context = {
        'profiles': Profile.objects.all()
    }
    return render(request, 'matchmaker/matches.html', context)


@ensure_csrf_cookie
def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'users/register.html')


@ensure_csrf_cookie
def login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'users/login.html')
