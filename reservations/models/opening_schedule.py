from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import time

class OpeningSchedule(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='opening_schedules')
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    sessions = ArrayField(ArrayField(models.TimeField(), size=2), default=list, blank=True)

    def add_session(self, open_time, close_time):
        if isinstance(open_time, str):
            open_time = time.fromisoformat(open_time)
        if isinstance(close_time, str):
            close_time = time.fromisoformat(close_time)
        
        self.sessions.append([open_time, close_time])
        self.sessions.sort(key=lambda x: x[0])
        self.save()

    def __str__(self):
        return f"{self.day}: " + ", ".join([f"{open_time.strftime('%H:%M')} - {close_time.strftime('%H:%M')}" for open_time, close_time in self.sessions])
