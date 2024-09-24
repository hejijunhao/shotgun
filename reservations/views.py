# reservations/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from .models import Table, Reservation
from .forms import ReservationForm
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F
from django.utils.safestring import mark_safe
from django.utils import timezone
import json

# Existing imports for API endpoints (if you still need them)
from rest_framework import viewsets
from .serializers import TableSerializer, ReservationSerializer

def home(request):
    return render(request, 'reservations/home.html')

def index(request):
    # The equivalent of Flask's index view
    return render(request, 'index.html', {'title': 'Home'})

def reservation_list(request):
    # List all reservations
    reservations = Reservation.objects.all().select_related('guest').prefetch_related('tables')
    context = {'reservations': reservations}
    return render(request, 'reservations/reservation_list.html', context)

def reservation_detail(request, pk):
    # Show reservation details
    reservation = get_object_or_404(Reservation, pk=pk)
    context = {'reservation': reservation}
    return render(request, 'reservations/reservation_detail.html', context)

def create_reservation(request):
    # Create a new reservation
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect('reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm()
    context = {'form': form}
    return render(request, 'reservations/create_reservation.html', context)

def restaurant_calendar(request):
    # Get all tables
    tables = list(Table.objects.all().values('id', 'number'))

    # Get reservations for today or for a selected date
    date_str = request.GET.get('date')
    if date_str:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()

    reservations = list(
        Reservation.objects.filter(
            start_datetime__date=selected_date
        ).select_related('guest').values(
            'id', 'guest__name', 'start_datetime', 'end_datetime', 'tables__number'
        )
    )

    # Generate time slots (e.g., from 10:00 AM to 10:00 PM in 30-minute intervals)
    time_slots = []
    start_time = datetime.combine(selected_date, datetime.strptime('10:00', '%H:%M').time())
    end_time = datetime.combine(selected_date, datetime.strptime('22:00', '%H:%M').time())
    current_time = start_time
    while current_time < end_time:
        time_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=30)

    context = {
        'tables': tables,
        'time_slots': time_slots,
        'reservations': json.dumps(reservations, cls=DjangoJSONEncoder),
        'selected_date': selected_date,
    }

    return render(request, 'reservations/restaurant_calendar.html', context)

# If you still need the API endpoints
class TableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer