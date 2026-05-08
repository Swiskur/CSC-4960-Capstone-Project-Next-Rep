from django.shortcuts import render, redirect
from .models import TrainerAvailability, User, Appointment
from .forms import TrainerAvailabilityForm, RegistrationForm, AppointmentForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail


# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def SignUp(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'athlete'
            user.save()
            login(request, user, backend='main.auth_backends.EmailOrUsernameModelBackend')
            # Redirect based on role
            if user.role == 'trainer':
                return redirect('trainer_dashboard')
            return redirect('athlete_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'main/sign_up.html', {'form': form})

def LogIn(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is None:
                messages.error(request, "Invalid email or password.")
            else:
                login(request, user)
                if user.role == 'trainer':
                    return redirect('trainer_dashboard')
                return redirect('athlete_dashboard')
    else:
        form = LoginForm()
    return render(request, 'main/log_in.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def trainer_dashboard(request):
    #If an athlete tries accessing then it will redirct them to the athlete dashbaord
    if request.user.role != 'trainer':
        return redirect('athlete_dashboard')
    
    appointments = Appointment.objects.filter(
        trainer=request.user,
        end_time__gte=timezone.now()

    ).exclude(status='canceled').order_by('start_time')
    return render(request, 'main/trainer_dashboard.html', {'appointments': appointments,})

@login_required(login_url='log_in')
def trainer_avail(request):

    #If an athlete tries accessing then it will redirct them to the athlete dashbaord
    if request.user.role != 'trainer':
        return redirect('athlete_dashboard')

    #Trainer user
    trainer = request.user

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
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    options = TrainerAvailability.objects.filter(
        trainer=trainer
    ).filter(
        Q(date__gt=today) | Q(date=today, end_time__gte=current_time)
    ).order_by('date', 'start_time')


    #Renders the trainer_availability page as well as the form and options
    return render(request, 'main/trainer_availability.html',{
        'form': form, 
        'options': options,
    })

@login_required(login_url='log_in')
def athlete_dashboard(request):
   
   
   #Restricts access to athletes only
   if request.user.role != 'athlete':
       return redirect('trainer_dashboard')
   
   trainers = User.objects.filter(role='trainer')
   athlete = request.user
   appointments = Appointment.objects.filter(
        athlete=athlete,
        end_time__gte=timezone.now()
    ).exclude(status='canceled').order_by('start_time')
   return render(request, 'main/athlete_dashboard.html', {'trainers': trainers, 'appointments': appointments})

@login_required(login_url='log_in')
def trainer_open_appointments(request, trainer_id):

    #Restricts access to Athletes only
    if request.user.role != 'athlete':
       return redirect('trainer_dashboard')
   
    #Retrieves the trainer selected
    trainer = get_object_or_404(User, id=trainer_id, role='trainer')

    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    #Available appointments for the trainer
    appointments_avail = TrainerAvailability.objects.filter(
        trainer=trainer,
        is_booked=False
    ).filter(
        Q(date__gt=today) | Q(date=today, end_time__gte=current_time)
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

            #Athlete user
            athlete = request.user

            #Creates an appointment for the athlete from their selection
            appointment = Appointment.objects.create(
                athlete=athlete,
                trainer=trainer,
                availability=appt,
                start_time=datetime.combine(appt.date, appt.start_time),
                end_time=datetime.combine(appt.date, appt.end_time),
                notes=form.cleaned_data['notes'],
            )
            
            #Adds email Subject
            subject = 'NextRep Appointment Booked'

            #Creates a standard email message with appointment information
            message = (
                f"Appointment Successfully Booked.\n\n"
                f"{appointment.athlete.username} with {appointment.trainer.username}\n"
                f"On {appointment.start_time.strftime('%A, %B, %d, %Y')}\n"
                f"From {appointment.start_time.strftime('%I: %M %p')} - {appointment.end_time.strftime('%I: %M %p')}\n"
                f"Notes: {appointment.notes or 'No notes.'}"   
            )

            #Recipients for the email
            recipient_list = [
                appointment.athlete.email,
                appointment.trainer.email,
            ]

            #Sends the email
            send_mail(
                subject,
                message,
                None,
                recipient_list,
                fail_silently=False

            )

            #The appointment is booked
            appt.is_booked = True
            appt.save()

            #Redirects user to the trainer's open appointments page
            return redirect('athlete_dashboard')
        
    #Renders page with the trainers available information and form
    return render(request, 'main/available_appointments.html', {
        'trainer': trainer,
        'appointments_avail': appointments_avail,
        'form': form,
    })

#Canceled Function
@login_required(login_url='login')
def cancel_appointment(request, appointment_id):

    #Retrieves the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)

    #User restrictions for athletes and trainers only
    if request.user != appointment.athlete and request.user != appointment.trainer:
        return redirect('home')


    #Changing appointment status to canceled
    appointment.status = 'canceled'
    appointment.save()

    #Making canceled appointments available again
    if appointment.availability:
        appointment.availability.is_booked = False
        appointment.availability.save()
    
    #Redirecting users to their dashboards
    if request.user.role == 'trainer':
        return redirect('trainer_dashboard')
    if request.user.role == 'athlete':
        return redirect('athlete_dashboard')
    
def calendar(request):
    return render(request, 'main/calendar.html')

        