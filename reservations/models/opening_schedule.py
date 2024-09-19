from django.db import models
from datetime import time

class OpeningSchedule:
    def __init__(self):
        self.schedule = {
            'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [],
            'Friday': [], 'Saturday': [], 'Sunday': []
        }

    def add_session(self, day, open_time, close_time):
        if isinstance(open_time, str):
            open_time = time.fromisoformat(open_time)
        if isinstance(close_time, str):
            close_time = time.fromisoformat(close_time)
        
        self.schedule[day].append((open_time, close_time))
        self.schedule[day].sort(key=lambda x: x[0])  # Sort sessions by start time

    def get_sessions(self, day):
        return self.schedule[day]

    def is_open(self, day, check_time):
        if isinstance(check_time, str):
            check_time = time.fromisoformat(check_time)
        
        for open_time, close_time in self.schedule[day]:
            if open_time <= check_time < close_time:
                return True
        return False

    def __str__(self):
        schedule_str = ""
        for day, sessions in self.schedule.items():
            schedule_str += f"{day}: "
            if sessions:
                schedule_str += ", ".join([f"{open_time.strftime('%I:%M %p')} - {close_time.strftime('%I:%M %p')}" 
                                           for open_time, close_time in sessions])
            else:
                schedule_str += "Closed"
            schedule_str += "\n"
        return schedule_str