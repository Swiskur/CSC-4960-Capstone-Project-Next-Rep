# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up/', views.SignUp, name='sign_up'),
    path('login/', views.LogIn, name='log_in'),
    path('trainer-avail/', views.trainer_avail, name='trainer_avail'),
    path('athlete-dashboard/', views.athlete_dashboard, name='athlete_dashboard'),
    path('trainer-dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer-open-appointments/<int:trainer_id>/', views.trainer_open_appointments, name='trainer_open_appointments'),
    path('logout/', views.logout_view, name='logout'),
    path('calendar/', views.calendar, name='calendar')

]