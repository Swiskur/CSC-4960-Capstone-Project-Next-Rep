from django.shortcuts import render, redirect
from .models import TrainerAvailability, User
from .forms import TrainerAvailabilityForm

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def SignUp(request):
    return render(request, 'main/sign_up.html')

def LogIn(request):
    return render(request, 'main/log_in.html')
def trainer_avail(request):
    if request.method == 'POST':
        form = TrainerAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)

            trainerU = User.objects.filter(role='trainer').first()
            availability.trainer = trainerU

            availability.save()

            return redirect('trainer_avail')
    else:
        form = TrainerAvailabilityForm()

    options = TrainerAvailability.objects.all()

    return render(request, 'main/trainer_availability.html',{
        'form': form, 
        'options': options,
    })