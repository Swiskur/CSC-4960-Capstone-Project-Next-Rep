# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up/', views.SignUp, name='sign_up'),
    path('login/', views.LogIn, name='log_in'),
    path('trainer-avail/', views.trainer_avail, name='trainer_avail'),


]