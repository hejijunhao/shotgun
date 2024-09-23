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
        self.max_capacity_utilized = False  # Reset the flag

        if not self.start_datetime:
            raise ValidationError("Start datetime must be specified.")

        if not self.duration:
            raise ValidationError("Duration must be specified.")

        if self.duration.total_seconds() <= 0:
            raise ValidationError('Duration must be a positive value.')

        self.end_datetime = self.start_datetime + self.duration

        tables = self.tables.all()

        if not tables:
            raise ValidationError("At least one table must be selected.")

        # Prevent double bookings
        overlapping_reservations = Reservation.objects.filter(
            tables__in=tables,
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime,
        ).exclude(id=self.id).distinct()

        if overlapping_reservations.exists():
            raise ValidationError("One or more tables are already booked for the selected time.")

        # Check if tables are merged
        if len(tables) > 1:
            # Multiple tables selected
            # Check if all selected tables are merged together
            merged_tables_set = set(tables)
            all_tables_merged = all(
                merged_tables_set <= set(table.merged_with.all()) | {table}
                for table in tables
            )
            if all_tables_merged:
                # Use merged capacity
                total_capacity = sum(table.merged_capacity for table in tables)
                if self.party_size > total_capacity:
                    raise ValidationError("Merged tables cannot accommodate the party size.")
            else:
                # Tables are not merged together, sum default capacities
                total_capacity = sum(table.default_capacity for table in tables)
                if self.party_size > total_capacity:
                    raise ValidationError("Selected tables cannot accommodate the party size.")
        else:
            # Single table selected
            table = tables[0]
            if table.merged_with.exists():
                # Table is merged with others, use merged capacity
                total_capacity = table.merged_capacity
                if self.party_size > total_capacity:
                    raise ValidationError("Merged table cannot accommodate the party size.")
            else:
                # Table is not merged, apply capacity logic
                if self.party_size <= table.default_capacity:
                    # No issue
                    pass
                elif self.party_size <= table.max_capacity:
                    # Max capacity utilized
                    self.max_capacity_utilized = True
                else:
                    raise ValidationError("Selected table cannot accommodate the party size.")

    def save(self, *args, **kwargs):
        self.full_clean()
        # Ensure end_datetime is correctly calculated
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