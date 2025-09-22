
# booking/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_location', 'end_location', 'date', 'time', 'name', 'phone', 'email']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'start_location': forms.TextInput(attrs={
                'placeholder': 'Ange startplats (ex: Storgatan 15)',
                'class': 'form-control'
            }),
            'end_location': forms.TextInput(attrs={
                'placeholder': 'Ange destination (ex: Centralstation)',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Ange ditt namn',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Ange ditt telefonnummer',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ange din e-postadress',
                'class': 'form-control'
            }),
        }
        labels = {
            'start_location': 'Från',
            'end_location': 'Till',
            'date': 'Datum',
            'time': 'Tid',
            'name': 'Namn',
            'phone': 'Telefonnummer',
            'email': 'E-post (för bekräftelse)',
        }

class DriverLoginForm(forms.Form):
    username = forms.CharField(
        label='Användarnamn',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ange användarnamn',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Lösenord',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ange lösenord',
            'class': 'form-control'
        })
    )
