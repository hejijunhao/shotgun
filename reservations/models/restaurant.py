# models/restaurant.py

from .opening_schedule import OpeningSchedule

class Restaurant:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.opening_schedule = OpeningSchedule()
        self.tables = []

    def add_table(self, table):
        self.tables.append(table)

    def get_tables(self):
        return self.tables

    def get_available_tables(self, party_size):
        return [table for table in self.tables if table.is_available() and table.can_accommodate(party_size)]

    def add_opening_session(self, day, open_time, close_time):
        self.opening_schedule.add_session(day, open_time, close_time)

    def is_open(self, day, time):
        return self.opening_schedule.is_open(day, time)

    def __str__(self):
        return f"{self.name} at {self.address}\n\nOpening Hours:\n{self.opening_schedule}"