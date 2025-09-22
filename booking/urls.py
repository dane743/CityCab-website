
# booking/urls.py
from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('boka/', views.booking_form, name='booking_form'),
    path('tack/', views.booking_success, name='booking_success'),
    path('driver/', views.driver_login, name='driver_login'),
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('driver/logout/', views.driver_logout, name='driver_logout'),
    path('booking/<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),
    path('booking/<int:booking_id>/decline/', views.decline_booking, name='decline_booking'),
]