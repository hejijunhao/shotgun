import re

class Guest:
    def __init__(self, name, phone, email):
        self.name = name
        self.set_phone(phone)
        self.set_email(email)

    def set_phone(self, phone):
        if self.validate_phone(phone):
            self.phone = phone
        else:
            raise ValueError("Invalid phone number format")

    def set_email(self, email):
        if self.validate_email(email):
            self.email = email
        else:
            raise ValueError("Invalid email format")

    @staticmethod
    def validate_phone(phone):
        # Basic phone validation (adjust regex as needed for your specific format)
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        return bool(phone_pattern.match(phone))

    @staticmethod
    def validate_email(email):
        # Basic email validation
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(email))

    def __str__(self):
        return f"Guest: {self.name}, Phone: {self.phone}, Email: {self.email}"