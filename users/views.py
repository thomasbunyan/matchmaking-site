from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, QueryDict
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileUpdateCreate
from .models import User, Profile, Hobby

from datetime import date
from django.utils.timezone import now

import json


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

    # Just increasing view counter on viewing profile here, need to do it for ajax as well
    request.user.profile.views = request.user.profile.views+1
    request.user.save()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'views': request.user.profile.views,
        'heat': request.user.profile.user_heat.count()
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

# Get individual profiles by specifying the ID, specifying nothing will return own profile


@login_required
def apiProfile(request, userid=None):
    try:
        
        # Uploading profile pics required a seprate HTTP endpoint, due to file encoding. 
        if request.method == "POST":
            profile = User.objects.get(id=request.user.id).profile
            image = request.FILES['file-0']
            profile.image = image
            profile.save()
            return JsonResponse({"success": True})

        # Get Individual Profiles or Current profile    
        if request.method == "GET":
            if userid:
                profile = User.objects.get(id=userid).profile
                # Increase counter every time you make call to get individual profile if not user
                profile.views = profile.views+1
                # Save user changes
                profile.save()
            else:
                profile = User.objects.get(id=request.user.id).profile

            hobbies = []
            for hobby in profile.hobbies.all():
                hobbies.append(hobby.name)

            jsonProduct = {'id': profile.user.id,
                                'image': '/media/' + str(profile.image),
                                'firstname': profile.user.first_name,
                                'lastname': profile.user.last_name,
                                'email': profile.user.email,
                                'dob': profile.dob.strftime('%Y-%m-%d'),
                                'gender': profile.gender,
                                'location': profile.location,
                                'description': profile.description,
                                'adjectives': profile.adjectives,
                                'views': str(profile.views),
                                'heat': profile.user_heat.count()
            }

            jsonProduct['hobbies'] = hobbies

            # !!!!!!!!!!!!!! newHeats doesn't exist.!!!!!!!!!!!!!!!!
            # Use newheats to notify user within app of new heat alerts
            # if newHeats != None:
            #     jsonProduct['newheats'] = newHeats

            jsonData = json.dumps(jsonProduct)
            return HttpResponse(jsonData, content_type="application/json")

        # Update your profile
        if request.method == "PUT":
            request.PUT = QueryDict(request.body)  
            hobbyPks = request.PUT.getlist('hobbies[]')
            hobbies = Hobby.objects.filter(pk__in=hobbyPks)

            print(request.FILES)

            u_form = UserUpdateForm(request.PUT, instance=request.user)
            p_form = ProfileUpdateForm(
            request.PUT, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                request.user.profile.hobbies.set(hobbies)
                return JsonResponse({"success": True, "redirect": "profile/"})
            else:
                return JsonResponse({"success": False})
        else:
            return JsonResponse({"success": False})
    except:
        return JsonResponse({"success": False})

@login_required
def apiProfiles(request):
    if request.method == "GET":
        # Query Filter are lazily evaluated
        current = now().date()
        minAge = request.GET.get('minAge')
        maxAge = request.GET.get('maxAge')
        gender = request.GET.get('gender')

        # If set will return only the people you are matching with that like you back
        matches = request.GET.get('matches')

        if matches:
            res = request.user.profile.user_heat.all() & request.user.profile.heat.all()
        else:
            res = Profile.objects.exclude(user=request.user.id)

        if minAge:
            minAge = int(minAge)
            min_date = date(current.year - minAge, current.month, current.day)
            res = res.filter(dob__lte=min_date)
            

        if maxAge:
            maxAge = int(maxAge)
            max_date = date(current.year - maxAge, current.month, current.day)
            res = res.filter(dob__gte=max_date)

        if gender:
            if gender == "M":
                res = res.filter(gender = 'M')
            else:
                res = res.filter(gender = 'F')
            
        # Manually Making Json File
        # res = serializers.serialize('json', res)

        # Hashmap for all the ones that you have favourited
        favorited = []
        for profile in request.user.profile.heat.all():
            favorited.append(profile.id)
        
        userhobbies = []
        for hobby in request.user.profile.hobbies.all():
            userhobbies.append(hobby.name)
 
        jsonData = []
        
        for profile in res:

            # Temp fix for dates
            # if(profile.dob):
            #     dob = profile.dob.strftime('%Y-%m-%d')
            # else:
            #     dob = "N/A"

            jsonProduct = { 'id' : profile.user.id,
                            'image': '/media/' + str(profile.image),
                            'firstname': profile.user.first_name,
                            'lastname' : profile.user.last_name,
                            'dob' : profile.dob.strftime('%Y-%m-%d'),
                            'gender' : profile.gender,
                            'location': profile.location,
                            'description' : profile.description,
                            'adjectives' : profile.adjectives,
                            'views' : str(profile.views),             
            }

            hobbies = []
            chobbies = 0
            for hobby in profile.hobbies.all():
                hobbies.append(hobby.name)
                if(hobby.name in userhobbies):
                    chobbies = chobbies + 1
            
            jsonProduct['hobbies'] = hobbies
            jsonProduct['commonhobbies'] = chobbies

            if(profile.id in favorited):
                jsonProduct['heat'] = True
            else:
                jsonProduct['heat'] = False

            jsonData.append(jsonProduct)
            
        # return JsonResponse(jsonData, safe=False)

        # Sort the json data by common hobbies
        jsonData = sorted(jsonData, key=lambda k: k['commonhobbies'], reverse=True)
        jsonData = json.dumps(jsonData)
        return HttpResponse(jsonData, content_type="application/json")

    return JsonResponse({"success": False})


def apiHobby(request, id):
    if request.method == "GET":
        res = Hobby.objects.filter(pk=id)
        res = serializers.serialize('json', res)
        return HttpResponse(res, content_type="application/json")

    return JsonResponse({"success": False})


def apiHobbies(request):
    if request.method == "GET":
        res = Hobby.objects.all()
        res = serializers.serialize('json', res)
        return HttpResponse(res, content_type="application/json")


def apiRegister(request):
    if request.method == "POST":
        uform = UserRegisterForm(request.POST)
        pformt = ProfileUpdateCreate(request.POST)
        
        if uform.is_valid() and pformt.is_valid():
            print("valid")
            uform.save()
            user = uform.instance
            pform = ProfileUpdateCreate(request.POST, instance=user.profile)
            pform.save()

            # pform.user = uform
            # pform.save()
            print(uform)
            print(pform)

            # Welcome Email Details
            firstName = user.first_name
            lastName = user.last_name
            email = user.email
            subject = 'Thank you for registering with MatchMaker!'
            fromemail = 'no-reply@neshanthan.com'

            context = {
                'firstName' : firstName,
                'lastName' : lastName
            }

            # Send Email to user when new heat recieved
            send_mail(
                subject,
                render_to_string('emails/welcome.txt', context),
                fromemail,
                [email],
                fail_silently=False,
            )

            return JsonResponse({"success": True, "redirect": "login/"})
        else:
            print("not valid")
            return JsonResponse({"success": False, "errors": str(uform.errors) + " " + str(pform.errors)})
    else:
        return JsonResponse({"success": False})

@login_required
def apiNotifications(request):
    profile = User.objects.get(id=request.user.id).profile
    # If user then change prevHeats and tell user how many new ones since last time
    newHeats = profile.user_heat.count()-profile.prevHeat
    profile.prevHeat = profile.user_heat.count()

    # Newmatches
    newMatches = profile.newMatches
    profile.newMatches = 0

    profile.save()

    return JsonResponse({"newheats": newHeats, "newmatches": newMatches})
    



@login_required
def apiProfileIDHeat(request):
    if request.method == "POST":
        # request.PUT = QueryDict(request.body)
        if(request.POST.get("username") != None):
            username = request.POST['username']
            profile = Profile.objects.get(user=username)
            request.user.profile.heat.add(profile)
            
            # If the user being liked likes the person liking him then add new like notification on both
            if request.user.profile in profile.user_heat: 
                request.user.profile.newMatches += 1
                profile.newMatches += 1 

            # Save Changes
            request.user.profile.save()
            profile.save()

            # Email Details
            firstName = profile.user.first_name
            lastName = profile.user.last_name
            email = profile.user.email
            subject = 'Someone has given you some heat!'
            fromemail = 'no-reply@neshanthan.com'

            context = {
                'firstName' : firstName,
                'lastName' : lastName
            }

            # Send Email to user when new heat recieved
            send_mail(
                subject,
                render_to_string('emails/newheat.txt', context),
                fromemail,
                [email],
                fail_silently=False,
            )

            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})

    elif request.method == "DELETE":
        delete = QueryDict(request.body)
        if(delete.get("username") != None):
            username = delete['username']
            profile = Profile.objects.get(user=username)
            request.user.profile.heat.remove(profile)

            # take away 1 from prevHeat so you will get notfication on new heats
            profile.prevHeat = profile.prevHeat-1
            profile.save() 

            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})
