from django.urls import path
from reservations.views.home_views import home, index, main_calendar
from reservations.views.reservation_views import reservation_list, reservation_detail, create_reservation
from reservations.views.calendar_views import restaurant_calendar

urlpatterns = [
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('main/', main_calendar, name='main_calendar'),  # New URL for the main calendar
    path('reservations/', reservation_list, name='reservation_list'),
    path('reservations/<int:pk>/', reservation_detail, name='reservation_detail'),
    path('reservations/create/', create_reservation, name='create_reservation'),
    path('calendar/', restaurant_calendar, name='restaurant_calendar'),
]
