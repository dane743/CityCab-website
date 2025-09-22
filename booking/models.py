
# booking/models.py
from django.db import models
from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Väntar'),
        ('accepted', 'Accepterad'),
        ('declined', 'Avböjd'),
    ]
    
    start_location = models.CharField('Från', max_length=255)
    end_location = models.CharField('Till', max_length=255)
    date = models.DateField('Datum')
    time = models.TimeField('Tid')
    name = models.CharField('Namn', max_length=100)
    phone = models.CharField('Telefonnummer', max_length=20)
    email = models.EmailField('E-post', max_length=254)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Skapad', auto_now_add=True)
    updated_at = models.DateTimeField('Uppdaterad', auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bokning'
        verbose_name_plural = 'Bokningar'
    
    def __str__(self):
        return f"{self.name} - {self.start_location} till {self.end_location}"
