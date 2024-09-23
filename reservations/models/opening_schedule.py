from django.db import models
from django.core.exceptions import ValidationError

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
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        related_name='opening_schedules'
    )
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    active = models.BooleanField(default=False)  # Active or Inactive

    def clean(self):
        super().clean()
        sessions_count = self.sessions.count()
        if self.active and sessions_count == 0:
            raise ValidationError('Active days must have at least one session.')
        if not self.active and sessions_count > 0:
            raise ValidationError('Inactive days should not have any sessions.')

    def __str__(self):
        sessions_str = ", ".join([str(session) for session in self.sessions.all()])
        return f"{self.day}: {sessions_str if sessions_str else 'No sessions'}"
