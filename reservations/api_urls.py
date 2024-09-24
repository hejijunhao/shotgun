from django.urls import path, include
from rest_framework import routers
from .views import TableViewSet, ReservationViewSet

router = routers.DefaultRouter()
router.register(r'tables', TableViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]