from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/create/', views.create_reservation, name='create_reservation'),
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('calendar/', views.restaurant_calendar, name='restaurant_calendar'),
    path('api/', include('reservations.api_urls')),  # Include if needed
    path('index/', views.index, name='index'),
]
