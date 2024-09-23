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
    active = models.BooleanField(default=False)
    sessions = models.ManyToManyField('Session', blank=True)

    def __str__(self):
        return f"{self.day}: {', '.join(str(session) for session in self.sessions.all()) or 'No sessions'}"


    def clean(self):
        super().clean()
        if self.pk:
            if self.active and self.sessions.count() == 0:
                raise ValidationError('Active days must have at least one session.')
