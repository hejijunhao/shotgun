from django.db import models
from .table import Table
from .opening_schedule import OpeningSchedule

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
    def add_table(self, number, capacity, mergable=False):
        return Table.objects.create(restaurant=self, number=number, capacity=capacity, mergable=mergable)

    def get_tables(self):
        return self.tables.all()

    def get_available_tables(self, party_size):
        return self.tables.filter(merged_with__isnull=True).filter(capacity__gte=party_size)

    def add_opening_session(self, day, open_time, close_time):
        schedule, created = OpeningSchedule.objects.get_or_create(restaurant=self, day=day)
        schedule.add_session(open_time, close_time)

    def is_open(self, day, time):
        try:
            schedule = self.opening_schedules.get(day=day)
            return schedule.is_open(time)
        except OpeningSchedule.DoesNotExist:
            return False

    def __str__(self):
        return f"{self.name} at {self.address}"

    class Meta:
        app_label = 'reservations'