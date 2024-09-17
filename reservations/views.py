from django.shortcuts import render

def home(request):
    return render(request, 'reservations/home.html')

def reservation_list(request):
    # Add logic to list reservations
    return render(request, 'reservations/reservation_list.html')

def create_reservation(request):
    # Add logic to create a reservation
    return render(request, 'reservations/create_reservation.html')

def reservation_detail(request, pk):
    # Add logic to show reservation details
    return render(request, 'reservations/reservation_detail.html')