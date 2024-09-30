# reservations/views/calendar_views.py

from django.shortcuts import render
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from ..models import Table, Reservation
import json

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