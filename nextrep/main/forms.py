from django import forms
from .models import TrainerAvailability, Appointment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class TrainerAvailabilityForm(forms.ModelForm):
    class Meta:

        #connects to TrainerAvailability model
        model = TrainerAvailability

        #Creates fields from the model that appear in the form
        fields = ['date', 'start_time', 'end_time']

        #Customizes form UI in HTML
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:

        #Connects to Appointment model in db
        model = Appointment

        #creates a notes field
        fields = ['notes']

        #customizes the notes section
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Add notes such as injured area and syptoms'
            })
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@madonna.edu'):
            raise forms.ValidationError('You must use a Madonna University email address.')
        return email