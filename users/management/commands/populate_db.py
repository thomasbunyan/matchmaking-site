from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.core.management.commands import loaddata
from django.contrib.auth.models import User
from users.models import Profile, Hobby
import sys, os
import yaml
import json


class Command(BaseCommand):
    args = 'No Arguments Accepted right now'
    help = 'Use this to reset the database users'

    def _create_data(self):
        mainpath = os.path.join(sys.path[0], 'fixtures')
        profilesfilepath = os.path.join(mainpath, 'profiles.yaml')
        profiles = yaml.load(open(profilesfilepath)) 
        hobbiesfilepath = os.path.join(mainpath, 'hobbies.yaml')
        hobbies = yaml.load(open(hobbiesfilepath))
        usersfilepath = os.path.join(mainpath, 'users.yaml')

        #Reset All data
        Print("Resetting All Data")
        management.call_command('flush', verbosity=0, interactive=False)

        #Create the users
        Print("Creating all user accounts")
        management.call_command('loaddata', usersfilepath, verbosity=0)

        #Create the hobbies
        Print("Creating all hobbies")
        management.call_command('loaddata', hobbiesfilepath, verbosity=0)

        #Load up the hobbies
        allHobbies = {}
        for hobby in hobbies:
            hobbyname = hobby["fields"]["name"]
            hobby = Hobby.objects.get_by_natural_key(hobbyname)
            allHobbies[hobbyname] = hobby

        #Add the new profile data
        for profile in profiles:
            if profile["model"] == "users.profile":
                usernk = profile["fields"]["user"][0]
                user=User.objects.get_by_natural_key(usernk)
                user.profile.image = profile["fields"]["image"]
                user.profile.gender = profile["fields"]["gender"]
                user.profile.description = profile["fields"]["description"]
                user.profile.location = profile["fields"]["location"]
                user.profile.dob = profile["fields"]["dob"]
                user.profile.adjectives = profile["fields"]["adjectives"]
                user.profile.views = profile["fields"]["views"]
                user.profile.prevHeat = profile["fields"]["prevHeat"]
                user.profile.newMatches = profile["fields"]["newMatches"]

                #For hobbies listed set it on user
                for hobby in profile["fields"]["hobbies"][0]:
                    user.profile.hobbies.add(allHobbies[hobby])

                #For All heated users add
                for heated in profile["fields"]["heat"]:
                    heateduser = User.objects.get_by_natural_key(heated[0])
                    user.profile.heat.add(heateduser.profile)
                    
                user.save()
                print("Modified profile for User: " + usernk)
                

    def handle(self, *args, **options):
        self._create_data()