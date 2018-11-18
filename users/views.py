from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Hobby


@login_required
def profile(request):



    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    #Just increasing view counter on viewing profile here, need to do it for ajax aswell
    request.user.profile.views = request.user.profile.views+1
    request.user.save()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'views' : request.user.profile.views,
        'heat'  :request.user.profile.user_heat.count()
    }

    return render(request, 'users/profile.html', context)


def apiLogin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            return JsonResponse({"success": True, "redirect": "profile"})
        else:
            return JsonResponse({"success": False})


def apiProfile(request):
    if request.method == "GET":
        res = Profile.objects.filter(user=request.user.id)
        res = serializers.serialize('json', res)
        return HttpResponse(res, content_type="application/json")

    return JsonResponse({"success": False})


def apiProfiles(request):
    if request.method == "GET":
        res = Profile.objects.exclude(user=request.user.id)
        res = serializers.serialize('json', res)
        return HttpResponse(res, content_type="application/json")

    return JsonResponse({"success": False})


def apiHobby(request, id):
    if request.method == "GET":
        res = Hobby.objects.filter(pk=id)
        res = serializers.serialize('json', res)
        return HttpResponse(res, content_type="application/json")

    return JsonResponse({"success": False})


def apiRegister(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("valid")
            form.save()
            return JsonResponse({"success": True, "redirect": "login/"})
        else:
            print("not valid")
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        return JsonResponse({"success": False})

@login_required
def apiProfileIDHeat(request):
    if request.method == "POST":
        #request.PUT = QueryDict(request.body)
        if(request.POST.get("username") != None):
            username = request.POST['username']
            user = Profile.objects.get(user=username)
            request.user.profile.heat.add(user)
            request.user.profile.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})

    elif request.method == "DELETE":
        if(request.POST.get("username") != None):
            username = request.GET['username']
            user = Profile.objects.get(user=username)
            request.user.profile.heat.remove(user)
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})
