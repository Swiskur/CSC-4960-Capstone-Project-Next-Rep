from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Appointment, TrainerAvailability


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("NextRep", {"fields": ("role", "sport", "microsoft_id")}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            ro.append("role")
        return ro


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("trainer", "athlete", "start_time", "end_time", "status")
    list_filter = ("status", "trainer")
    search_fields = ("trainer__username", "trainer__email", "athlete__username", "athlete__email")


@admin.register(TrainerAvailability)
class TrainerAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("trainer", "date", "start_time", "end_time", "is_booked")
    list_filter = ("trainer", "date", "is_booked")

