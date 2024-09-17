# reservations/urls.py
from django.urls import path
from . import views  # Import views from the app

urlpatterns = [
    path('', views.home, name='home'),  # Home page (existing)
    path('reservations/', views.reservation_list, name='reservation_list'),  # List reservations
    path('reservations/create/', views.create_reservation, name='create_reservation'),  # Create a reservation
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation_detail'),  # Reservation detail

    # Translated Flask views:
    path('index/', views.index, name='index'),  # Equivalent to Flask's index route
]
