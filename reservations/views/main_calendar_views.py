from django.shortcuts import render
import calendar
from datetime import datetime

def main_calendar_view(request):
    now = datetime.now()
    current_month = now.strftime('%B %Y')  # Example: September 2024
    num_days = calendar.monthrange(now.year, now.month)[1]
    days_in_month = list(range(1, num_days + 1))

    context = {
        'current_month': current_month,
        'days_in_month': days_in_month,
    }
    return render(request, 'main_calendar.html', context)