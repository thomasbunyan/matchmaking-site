from django.urls import path
from . import views as matchmaker_views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', matchmaker_views.home, name='matchmaker-home'),
    path('discover/', matchmaker_views.discover, name='matchmaker-discover'),
    path('mymatches/', matchmaker_views.matches, name='matchmaker-matches'),
    path('profile/', user_views.profile, name="profile"),
    path('register/', matchmaker_views.register, name="register"),
    path('login/', matchmaker_views.login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
]
