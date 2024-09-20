from django.db import models
from django.core.exceptions import ValidationError
import re

class Guest(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def clean(self):
        if not self.validate_phone(self.phone):
            raise ValidationError({'phone': 'Invalid phone number format'})

    @staticmethod
    def validate_phone(phone):
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        return bool(phone_pattern.match(phone))

    def __str__(self):
        return f"Guest: {self.name}, Phone: {self.phone}, Email: {self.email}"
