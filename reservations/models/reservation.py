import uuid
from datetime import timedelta
from django.db import models

class Guest(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_number = models.CharField(max_length=10)

    def __str__(self):
        return self.table_number

class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservations')
    party_size = models.IntegerField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    tables = models.ManyToManyField(Table)
    duration = models.DurationField(default=timedelta(hours=2))

    def save(self, *args, **kwargs):
        # Automatically calculate end_datetime when the reservation is saved
        self.end_datetime = self.start_datetime + self.duration
        super().save(*args, **kwargs)

    def update_duration(self, new_duration):
        self.duration = new_duration
        self.end_datetime = self.start_datetime + new_duration
        self.save()

    def update_tables(self, new_tables):
        self.tables.set(new_tables)

    def __str__(self):
        table_info = ', '.join([str(table.table_number) for table in self.tables.all()])
        return f"Reservation {self.id}: {self.guest.name}, Party of {self.party_size}, " \
               f"Table(s) {table_info}, {self.start_datetime.strftime('%Y-%m-%d %H:%M')} - " \
               f"{self.end_datetime.strftime('%H:%M')}"

    def to_dict(self):
        return {
            'id': str(self.id),
            'guest_name': self.guest.name,
            'party_size': self.party_size,
            'start_datetime': self.start_datetime.strftime('%Y-%m-%d %H:%M'),
            'end_datetime': self.end_datetime.strftime('%Y-%m-%d %H:%M'),
            'tables': [str(table.id) for table in self.tables.all()]
        }