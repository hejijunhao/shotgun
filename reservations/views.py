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
    tables = Table.objects.all()

    # Define the date for which to display reservations (e.g., today or selected date)
    date_str = request.GET.get('date')
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = datetime.now().date()

    # Generate time slots (e.g., from 10:00 AM to 10:00 PM in 30-minute intervals)
    start_time = datetime.combine(date, datetime.strptime('10:00', '%H:%M').time())
    end_time = datetime.combine(date, datetime.strptime('22:00', '%H:%M').time())
    time_slots = []
    current_time = start_time
    while current_time < end_time:
        time_slots.append(current_time)
        current_time += timedelta(minutes=30)

    # Get reservations for the selected date
    reservations = Reservation.objects.filter(
        start_datetime__date=date
    ).select_related('guest').prefetch_related('tables')

    # Convert tables to a list of dictionaries for serialization
    tables_data = list(tables.values('id', 'number'))

    # Map reservations to tables and time slots
    reservation_map = {}
    for reservation in reservations:
        res_start = reservation.start_datetime
        res_end = reservation.end_datetime
        res_times = []
        current_res_time = res_start
        while current_res_time < res_end:
            res_times.append(current_res_time)
            current_res_time += timedelta(minutes=30)
        for table in reservation.tables.all():
            for res_time in res_times:
                key = (table.id, res_time.strftime('%H:%M'))
                reservation_map[key] = reservation

    # Serialize reservations for JavaScript
    serialized_reservations = json.dumps(
        list(reservations.values(
            'id',
            'start_datetime',
            'end_datetime',
            guest_name=F('guest__name'),
            tables_numbers=ArrayAgg('tables__number'),
        )),
        cls=DjangoJSONEncoder
    )

    context = {
        'tables': tables_data,  # Pass the serialized table data
        'time_slots': time_slots,
        'reservation_map': reservation_map,
        'reservations_json': serialized_reservations,
        'selected_date': date,
    }
    return render(request, 'reservations/restaurant_calendar.html', context)

# If you still need the API endpoints
class TableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer