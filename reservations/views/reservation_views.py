# reservations/views/reservation_views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Reservation
from ..forms import ReservationForm

def reservation_list(request):
    reservations = Reservation.objects.all().select_related('guest').prefetch_related('tables')
    context = {'reservations': reservations}
    return render(request, 'reservations/reservation_list.html', context)

def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    context = {'reservation': reservation}
    return render(request, 'reservations/reservation_detail.html', context)

def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect('reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm()
    context = {'form': form}
    return render(request, 'reservations/create_reservation.html', context)
