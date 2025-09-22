
# booking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Booking
from .forms import BookingForm, DriverLoginForm

def home(request):
    """Homepage view"""
    return render(request, 'booking/home.html')

def booking_form(request):
    """Booking form view with customer email confirmation"""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # Send email notification to driver
            try:
                driver_subject = f'Ny taxibokning - {booking.name}'
                driver_message = f"""
Ny bokning har lagts till:

Från: {booking.start_location}
Till: {booking.end_location}
Datum: {booking.date}
Tid: {booking.time}
Namn: {booking.name}
Telefonnummer: {booking.phone}
E-post: {booking.email}

Logga in på förarportalen för att acceptera eller avböja bokningen.
                """
                
                send_mail(
                    driver_subject,
                    driver_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['sundsvallmiljotaxi@gmail.com'],  # Driver email
                    fail_silently=False,
                )
                
                # Send confirmation email to customer
                customer_subject = 'Din taxibokning har mottagits - CityCab'
                customer_message = f"""
Hej {booking.name}!

Tack för din bokning hos CityCab. Vi har mottagit följande bokningsförfrågan:

BOKNINGSDETALJER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Från: {booking.start_location}
📍 Till: {booking.end_location}
📅 Datum: {booking.date}
🕐 Tid: {booking.time}
👤 Namn: {booking.name}
📞 Telefon: {booking.phone}

NÄSTA STEG:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vår förare kommer att granska din bokning och kontakta dig inom kort för att bekräfta resan.

Du kommer att få ett nytt e-postmeddelande när föraren har accepterat din bokning.

Behöver du ändra eller avboka? Ring oss på 060-584-58-44.

Tack för att du väljer CityCab!

Med vänlig hälsning,
CityCab Team
Din pålitliga stadstaxi
                """
                
                send_mail(
                    customer_subject,
                    customer_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [booking.email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Din bokning har registrerats! Bekräftelse skickat till din e-post.')
                
            except Exception as e:
                messages.warning(request, 'Din bokning har registrerats, men e-postmeddelandet kunde inte skickas.')
            
            return redirect('booking:booking_success')
    else:
        form = BookingForm()
    
    return render(request, 'booking/booking_form.html', {'form': form})

def booking_success(request):
    """Booking success page"""
    return render(request, 'booking/booking_success.html')

def driver_login(request):
    """Driver login view"""
    if request.session.get('is_driver'):
        return redirect('booking:driver_dashboard')
    
    if request.method == 'POST':
        form = DriverLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if username == 'driver' and password == 'citycab2025':
                request.session['is_driver'] = True
                messages.success(request, 'Inloggning lyckades!')
                return redirect('booking:driver_dashboard')
            else:
                messages.error(request, 'Felaktiga inloggningsuppgifter.')
    else:
        form = DriverLoginForm()
    
    return render(request, 'booking/driver_login.html', {'form': form})

def driver_dashboard(request):
    """Driver dashboard view"""
    if not request.session.get('is_driver'):
        return redirect('booking:driver_login')
    
    bookings = Booking.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'booking/driver_dashboard.html', {'bookings': bookings})

def driver_logout(request):
    """Driver logout view"""
    if 'is_driver' in request.session:
        del request.session['is_driver']
    messages.success(request, 'Du har loggats ut.')
    return redirect('booking:home')

@require_POST
def accept_booking(request, booking_id):
    """Accept booking with customer notification"""
    if not request.session.get('is_driver'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'accepted'
    booking.save()
    
    # Send confirmation email to customer
    try:
        subject = 'Din taxibokning har accepterats! - CityCab'
        message = f"""
Hej {booking.name}!

GODA NYHETER! Din taxibokning har accepterats.

BOKNINGSDETALJER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Från: {booking.start_location}
📍 Till: {booking.end_location}
📅 Datum: {booking.date}
🕐 Tid: {booking.time}
📞 Din telefon: {booking.phone}

NÄSTA STEG:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Föraren kommer att kontakta dig på telefonnummer {booking.phone} för att bekräfta exakt upphämtningstid
✅ Var redo vid angiven tid på {booking.start_location}
✅ Ha ditt telefonnummer tillgängligt

Behöver du kontakta oss? Ring 060-584-58-44.

Tack för att du väljer CityCab!

Med vänlig hälsning,
CityCab Team
Din pålitliga stadstaxi
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.email],
            fail_silently=True,
        )
    except:
        pass
    
    messages.success(request, f'Bokning #{booking.id} accepterad! Kunden har meddelats via e-post.')
    return redirect('booking:driver_dashboard')

@require_POST
def decline_booking(request, booking_id):
    """Decline booking with customer notification"""
    if not request.session.get('is_driver'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'declined'
    booking.save()
    
    # Send decline notification to customer
    try:
        subject = 'Ang. din taxibokning - CityCab'
        message = f"""
Hej {booking.name}!

Tyvärr kan vi inte acceptera din bokningsförfrågan för följande resa:

BOKNINGSDETALJER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Från: {booking.start_location}
📍 Till: {booking.end_location}
📅 Datum: {booking.date}
🕐 Tid: {booking.time}

NÄSTA STEG:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 Ring oss direkt på 060-584-58-44 för att diskutera alternativ
🌐 Gör en ny bokning på vår hemsida för annan tid
💬 Vi hjälper dig gärna hitta en lösning

Vi ber om ursäkt för eventuella besvär och hoppas kunna hjälpa dig med framtida resor.

Med vänlig hälsning,
CityCab Team
Din pålitliga stadstaxi
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.email],
            fail_silently=True,
        )
    except:
        pass
    
    messages.info(request, f'Bokning #{booking.id} avböjd. Kunden har meddelats via e-post.')
    return redirect('booking:driver_dashboard')