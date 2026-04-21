from django.shortcuts import render, redirect
from .models import TrainerAvailability, User, Appointment
from .forms import TrainerAvailabilityForm, RegistrationForm, AppointmentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from datetime import datetime


# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def SignUp(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect based on role
            if user.role == 'trainer':
                return redirect('trainer_dashboard')
            return redirect('athlete_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'main/sign_up.html', {'form': form})

def LogIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'trainer':
                return redirect('trainer_dashboard')
            return redirect('athlete_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'main/log_in.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('log_in')

def trainer_dashboard(request):
    return render(request, 'main/trainer_dashboard.html')

def trainer_avail(request):

    #Temporary trainer made to test functionality
    trainer = User.objects.filter(role='trainer').first()

    #If POST request is made
    if request.method == 'POST':
        

        #Creates a form instance
        form = TrainerAvailabilityForm(request.POST)

        #If the vorm is valid
        if form.is_valid():

            #creates availability object that is assigned to the trainers availability and saves to the db
            availability = form.save(commit=False)
            availability.trainer = trainer
            availability.save()

            #redirects user to the same page
            return redirect('trainer_avail')
        
    
    else:

        #If the form is a GET request it creates a form
        form = TrainerAvailabilityForm()

    #All available options for the specific trainer
    options = TrainerAvailability.objects.filter(trainer=trainer)

    #Renders the trainer_availability page as well as the form and options
    return render(request, 'main/trainer_availability.html',{
        'form': form, 
        'options': options,
    })

def athlete_dashboard(request):
    trainers = User.objects.filter(role='trainer')


    return render(request, 'main/athlete_dashboard.html', {'trainers': trainers,})

def trainer_open_appointments(request, trainer_id):

    #Retrieves the trainer selected
    trainer = get_object_or_404(User, id=trainer_id, role='trainer')

    #Available appointments for the trainer
    appointments_avail = TrainerAvailability.objects.filter(
        trainer=trainer,
        is_booked=False
    ).order_by('date', 'start_time')

    #Creates an appointment form
    form = AppointmentForm()

    #If there is a POST request from the athlete
    if request.method == 'POST':

        #Finds the slot that was selected
        appt = get_object_or_404(
            TrainerAvailability,
            id=request.POST.get('appt_id'),
            trainer=trainer,
            is_booked=False
        )

        #Form hanldes the POST data
        form = AppointmentForm(request.POST)

        #If the form is valid
        if form.is_valid():

            #Creates a temporary athlete for testing
            athlete = User.objects.filter(role='athlete').first()

            #Creates an appointment for the athlete from their selection
            Appointment.objects.create(
                athlete=athlete,
                trainer=trainer,
                availability=appt,
                start_time=datetime.combine(appt.date, appt.start_time),
                end_time=datetime.combine(appt.date, appt.end_time),
                notes=form.cleaned_data['notes'],
            )

            #The appointment is booked
            appt.is_booked = True
            appt.save()

            #Redirects user to the trainer's open appointments page
            return redirect('trainer_open_appointments', trainer_id=trainer.id)
        
    #Renders page with the trainers available information and form
    return render(request, 'main/available_appointments.html', {
        'trainer': trainer,
        'appointments_avail': appointments_avail,
        'form': form,
    })
        