from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Restaurant, OpeningSchedule

@receiver(post_save, sender=Restaurant)
def create_opening_schedules(sender, instance, created, **kwargs):
    if created:
        days_of_week = [day[0] for day in OpeningSchedule.DAYS_OF_WEEK]
        for day in days_of_week:
            OpeningSchedule.objects.create(restaurant=instance, day=day)
