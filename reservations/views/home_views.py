# reservations/views/home_views.py

from django.shortcuts import render

def home(request):
    return render(request, 'reservations/home.html')

def index(request):
    return render(request, 'reservations/index.html')

# Add the new view for the main calendar
def main_calendar(request):
    return render(request, 'reservations/main_calendar.html')