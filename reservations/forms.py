# reservations/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        tables = cleaned_data.get('tables')
        start_datetime = cleaned_data.get('start_datetime')
        duration = cleaned_data.get('duration')
        party_size = cleaned_data.get('party_size')

        if not tables:
            raise ValidationError("At least one table must be selected.")

        if not start_datetime:
            raise ValidationError("Start datetime must be specified.")

        if not duration:
            raise ValidationError("Duration must be specified.")

        if duration.total_seconds() <= 0:
            raise ValidationError('Duration must be a positive value.')

        end_datetime = start_datetime + duration

        # Prevent double bookings
        overlapping_reservations = Reservation.objects.filter(
            tables__in=tables,
            start_datetime__lt=end_datetime,
            end_datetime__gt=start_datetime,
        ).exclude(id=self.instance.id).distinct()

        if overlapping_reservations.exists():
            raise ValidationError("One or more tables are already booked for the selected time.")

        # Initialize max_capacity_utilized flag
        self.instance.max_capacity_utilized = False

        # Capacity Checks
        if len(tables) > 1:
            # Handle merged tables
            merged_tables_set = set(tables)
            all_tables_merged = all(
                merged_tables_set <= set(table.merged_with.all()) | {table}
                for table in tables
            )
            if all_tables_merged:
                # Use merged capacity
                total_capacity = sum(table.merged_capacity for table in tables)
                if party_size > total_capacity:
                    raise ValidationError("Merged tables cannot accommodate the party size.")
            else:
                # Tables are not merged together, sum default capacities
                total_capacity = sum(table.default_capacity for table in tables)
                if party_size > total_capacity:
                    raise ValidationError("Selected tables cannot accommodate the party size.")
        else:
            # Single table selected
            table = tables[0]
            if table.merged_with.exists():
                # Table is merged with others, use merged capacity
                total_capacity = table.merged_capacity
                if party_size > total_capacity:
                    raise ValidationError("Merged table cannot accommodate the party size.")
            else:
                # Table is not merged, apply capacity logic
                if party_size <= table.default_capacity:
                    # No issue
                    pass
                elif party_size <= table.max_capacity:
                    # Max capacity utilized
                    self.instance.max_capacity_utilized = True
                else:
                    raise ValidationError("Selected table cannot accommodate the party size.")

        # Set the calculated end_datetime on the instance
        self.instance.end_datetime = end_datetime