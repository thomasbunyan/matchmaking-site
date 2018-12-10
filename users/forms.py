from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    dob = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name',  'email', 'password1', 'password2']


class ProfileUpdateCreate(forms.ModelForm):
    dob = forms.DateField(required=True)
    class Meta:
        model = Profile
        fields = ['dob']
        

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'gender', 'description',
                  'location', 'dob', 'hobbies', 'adjectives']
