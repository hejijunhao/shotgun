# reservations/models/reservation.py

from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.models import Q
import uuid
from .guest import Guest
from .table import Table


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name='reservations'
    )
    party_size = models.IntegerField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(editable=False)
    tables = models.ManyToManyField(Table)
    duration = models.DurationField(default=timedelta(hours=2))

    def clean(self):
        super().clean()

        if not self.start_datetime:
            raise ValidationError("Start datetime must be specified.")

        if not self.duration:
            raise ValidationError("Duration must be specified.")

        if self.duration.total_seconds() <= 0:
            raise ValidationError('Duration must be a positive value.')

        # Calculate end_datetime
        self.end_datetime = self.start_datetime + self.duration    

    def save(self, *args, **kwargs):
        self.full_clean()
        self.end_datetime = self.start_datetime + self.duration
        super().save(*args, **kwargs)

    def update_duration(self, new_duration):
        self.duration = new_duration
        self.end_datetime = self.start_datetime + new_duration
        self.save()

    def update_tables(self, new_tables):
        self.tables.set(new_tables)

    def __str__(self):
        table_info = ', '.join(
            [table.get_merged_identifier() for table in self.tables.all()]
        )
        return (
            f"Reservation {self.id}: {self.guest.name}, Party of {self.party_size}, "
            f"{table_info}, {self.start_datetime.strftime('%Y-%m-%d %H:%M')} - "
            f"{self.end_datetime.strftime('%H:%M')}"
        )

    def to_dict(self):
        return {
            'id': str(self.id),
            'guest_name': self.guest.name,
            'party_size': self.party_size,
            'start_datetime': self.start_datetime.strftime('%Y-%m-%d %H:%M'),
            'end_datetime': self.end_datetime.strftime('%Y-%m-%d %H:%M'),
            'tables': [str(table.id) for table in self.tables.all()]
        }