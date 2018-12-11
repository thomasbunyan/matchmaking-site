from django.urls import path
from . import views as api_views

urlpatterns = [
    path('profile/<int:userid>/', api_views.apiProfile, name="api-profile"),
    path('profile/', api_views.apiProfile, name="api-profile"),
    #path('profile/<int:id>/', api_views.apiProfileID, name="api-profile-id"),
    path('heat/', api_views.apiProfileIDHeat, name="api-profile-id-heat"),
    path('profiles/', api_views.apiProfiles, name="api-profiles"),
    path('hobby/<int:id>/', api_views.apiHobby, name="api-hobby"),
    path('hobbies/', api_views.apiHobbies, name="api-hobbies"),
    path('register/', api_views.apiRegister, name="api-register"),
    path('login/', api_views.apiLogin, name="api-login"),
    path('notifications/', api_views.apiNotifications, name="api-notifications"),
]
