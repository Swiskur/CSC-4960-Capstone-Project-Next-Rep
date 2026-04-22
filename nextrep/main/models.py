from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

def validate_madonna_email(value):
    value_lower = (value or "").lower()
    if not (value_lower.endswith('@madonna.edu') or value_lower.endswith('@my.madonna.edu')):
        raise ValidationError('You must use a Madonna University email address.')

class User(AbstractUser):

    #Gives role choices of either athlete or trainer
    ROLE_CHOICES = (
        ('athlete', 'Athlete'),
        ('trainer', 'Trainer'),
    )

    #Athletes select the sport they play based on Madonna sport options
    SPORT_CHOICES = (
        ('baseball', 'Baseball'),
        ('softball', 'Softball'),
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('track_field', 'Track & Field'),
        ('cross_country', 'Cross Country'),
        ('soccer', 'Soccer'),
        ('bowling', 'Bowling'),
        ('golf', 'Golf'),
        ('lacrosse', 'Lacrosse'),
        ('cheerleading', 'Cheerleading'),
        ('volleyball', 'Volleyball'),

    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='athlete')
    email = models.EmailField(unique=True, validators=[validate_madonna_email])
    sport = models.CharField(max_length=25, choices=SPORT_CHOICES, blank=True)

    #Function to only give athletes a sport value
    def save(self,*args, **kwargs):

        if self.role != 'athlete':
            self.sport = ''
        super().save(*args, **kwargs)

    #Returns username and role
    def __str__(self):
        return f"{self.username} ({self.role})"
    
class TrainerAvailability(models.Model):
    
    #Connects the trainer to availability
    trainer = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        limit_choices_to= {'role': 'trainer'},
        related_name= "availability"

    )

    #Saves date for availability
    date = models.DateField(null=True, blank=True)

    #Saves the day of week
    day_of_week = models.CharField(max_length=10, blank=True)

    #Saves the Start time and end time
    start_time = models.TimeField()
    end_time = models.TimeField()

    #Confirms when the appointment is booked
    is_booked = models.BooleanField(default=False)

    #Function used to fill in the day of the week when a date is selected
    def save(self, *args, **kwargs):
        if self.date:
            self.day_of_week = self.date.strftime('%A')
        super().save(*args, **kwargs)

    #Returns the trainer's availability
    def __str__(self):

        return f"{self.trainer.username} on {self.day_of_week}, {self.date} @ {self.start_time}-{self.end_time}"
    
class Appointment(models.Model):

    #Creates status options for an appointment
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    #Connects the athlete that is making the appointment
    athlete = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='athlete_appointments',
        limit_choices_to= {'role': 'athlete'},
    )

    #Connects the trainer that made the appointment
    trainer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='trainer_appointments',
        limit_choices_to= {'role': 'trainer'}
    )

    #Connects the appointment made to the trainer's availability
    availability = models.ForeignKey(
        TrainerAvailability,
        on_delete=models.CASCADE,
        related_name='appointments',
        null=True,
        blank=True
    )

    #Saves start time and end time
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    #Notes for athlete to fill in
    notes = models.TextField(blank=True)

    #Status of the appointment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    #Timestamps to tell when the appointment was created or updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #returns the appointment time with athlete and trainer
    def __str__(self):
        return f"{self.athlete} w/ {self.trainer} @ {self.start_time}"