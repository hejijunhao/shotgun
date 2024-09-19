from django.db import models
from datetime import datetime, timedelta

class Reservation:
    def __init__(self, guest, party_size, start_datetime, tables, duration=timedelta(hours=2)):
        self.id = str(uuid.uuid4())
        self.guest = guest
        self.party_size = party_size
        self.start_datetime = start_datetime
        self.end_datetime = start_datetime + duration
        self.set_tables(tables)

    def set_tables(self, tables):
        if isinstance(tables, (list, tuple)):
            self.tables = tables
        elif hasattr(tables, 'id'):  # Single table or MergedTable
            self.tables = [tables]
        else:
            raise ValueError("Invalid table(s) provided")

    def update_duration(self, new_duration):
        self.end_datetime = self.start_datetime + new_duration

    def update_tables(self, new_tables):
        self.set_tables(new_tables)

    def __str__(self):
        table_info = ', '.join([str(t.id) for t in self.tables])
        return f"Reservation {self.id}: {self.guest.name}, Party of {self.party_size}, " \
               f"Table(s) {table_info}, {self.start_datetime.strftime('%Y-%m-%d %H:%M')} - " \
               f"{self.end_datetime.strftime('%H:%M')}"

    def to_dict(self):
        return {
            'id': self.id,
            'guest_name': self.guest.name,
            'party_size': self.party_size,
            'start_datetime': self.start_datetime.strftime('%Y-%m-%d %H:%M'),
            'end_datetime': self.end_datetime.strftime('%Y-%m-%d %H:%M'),
            'tables': [t.id for t in self.tables]
        }