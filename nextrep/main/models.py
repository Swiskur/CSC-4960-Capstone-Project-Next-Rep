from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('athlete', 'Athlete'),
        ('trainer', 'Trainer'),

    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    microsoft_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class TrainerAvailability(models.Model):
    trainer = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        limit_choices_to= {'role': 'trainer'},
        related_name= "availability"

    )
    date = models.DateField(null=True, blank=True)
    day_of_week = models.CharField(max_length=10, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.date:
            self.day_of_week = self.date.strftime('%A')
        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.trainer.username} on {self.day_of_week}, {self.date} @ {self.start_time}-{self.end_time}"
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    athlete = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='athlete_appointments',
        limit_choices_to= {'role': 'athlete'},
    )
    trainer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='trainer_appointments',
        limit_choices_to= {'role': 'trainer'}
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.athlete} w/ {self.trainer} @ {self.start_time}"