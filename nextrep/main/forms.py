from django import forms
from .models import TrainerAvailability
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class TrainerAvailabilityForm(forms.ModelForm):
    class Meta:
        model = TrainerAvailability
        fields = ['date', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

