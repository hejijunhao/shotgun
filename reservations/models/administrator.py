from django.contrib.auth.hashers import make_password, check_password

class Administrator:
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = make_password(password)

    def check_password(self, password):
        return check_password(self.password_hash, password)
    
    def __str__(self):
        return f"Administrator: {self.username}"