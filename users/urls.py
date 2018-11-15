from django.urls import path
from . import views as api_views

urlpatterns = [
    path('profile/', api_views.apiProfile, name="api-profile"),
    path('profiles/', api_views.apiProfiles, name="api-profiles"),
    path('hobby/<int:id>/', api_views.apiHobby, name="api-hobby"),
    path('register/', api_views.apiRegister, name="api-register"),
    path('login/', api_views.apiLogin, name="api-login"),
]
