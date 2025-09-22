
# booking/admin.py
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_location', 'end_location', 'date', 'time', 'status', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['name', 'phone', 'start_location', 'end_location']
    ordering = ['-created_at']