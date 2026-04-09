from django.contrib import admin
from .models import User, Appointment, TrainerAvailability

admin.site.register(User)
admin.site.register(Appointment)
admin.site.register(TrainerAvailability)

